import enchant
import os

"""
    InvalidInputError exception
"""
class InvalidInputError(Exception):
    """
        Exception raised for invalid word provided by user
    """
    def __init__(self, message="Invalid response provided by user. Must be 'yes' 'no' 'y' or 'n'."):
        self.message = message
        super().__init__(self.message)

class InvalidWordError(Exception):
    """
        Exception raised for invalid word provided by user
    """
    def __init__(self, message="Invalid word was provied by the user"):
        self.message = message
        super().__init__(self.message)

#Using PyEnchant as valid word checker
spellcheck = enchant.Dict("en_US")

letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", " "]
points = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 4, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10, 0]
#Creates a dictionary based on zipping lists: letters (key) and points(value)
letter_to_points = {letter:points for letter, points in zip(letters, points)}

#Initialize list that will contain input players
players = []
#Initialize dict that will keep track of each player's points
player_to_points = {}
#Initialize dict that will keep track of each word a player has played
player_to_words = {}

"""
    Get number of players and player names based on user input.
"""
def get_players():
    try:
        num_players = int(input("How many players are playing: "))
        print()
    except ValueError:
        print()
        print("Please enter a valid number of players", end="\n\n")
        num_players = 0
        get_players()
    for i in range(num_players):
        players.append(input("Enter player name:  "))

"""
    Player (key) plays their word which is appended to the word list (value) 
    in player_to_words dict. First, validates the input is valid (all alpha
    charachters) with validate_input(), then checks the word is a valid US 
    English word with spell_check()
"""
def play_word(player):
    word = validate_input(player)
    result = spell_check(word, player)
    return result

"""
    Validates the input provided by the player doesn't contain any numbers
"""
def validate_input(player):
    while True:
        word = input(f"{player}'s turn. Please input a word: ")
        not_alpha = False
        for letter in word:
            if not(letter.isalpha()):
                if not(letter == " "):
                    print(f"Word can only contain letters. Try again, {player}!", end="\n\n")
                    not_alpha = True
                    break
        if not_alpha == True:
            continue
        elif len(word) == 0:
            print(f"No word was provided. Try again, {player}!", end="\n\n")
            continue
        return word

""" 
    Checks the word is a valid US English word using Pychant ('spellcheck' object). If so append to 
    player_to_words. If not raise InvalidWordError and recursively run play_word()
"""
def spell_check(original_word, player):
    word_with_blanks = get_blanks(original_word, player)
    word = list(word_with_blanks.keys())[0]
    blanks = list(word_with_blanks.values())[0]
    result = {}
    try:
        if spellcheck.check(word) == True:
            #handles KeyError if the list is initially empty
            result[word] = score_word(blanks)
            try:
                player_to_words[player].append(result)
            except KeyError:
                player_to_words[player] = []
                player_to_words[player].append(result)
        else:
            raise InvalidWordError
    except InvalidWordError:
        print(f"Invalid word! Must be a valid word from the English dictionary. Try again, {player}.", end="\n\n")
        play_word(player)

"""
    Checks if the provided word contains blanks and gets input from the user match the blank tiles with the corresponding letter. Checks if the input provided
    by the user is valid. Returs a dictionary with one item containing the full word (key) and the blank tile letter values (value)
"""
def get_blanks(word, player):
    if " " in word:
        while True:
            result = {}
            #keeps track of letter position in word
            word_count = 0
            #keeps track of letter position in blank_letters
            blank_count = 0
            #keeps track of blank tile letters in order they appear
            blank_letters = ""
            #create list from word to allow changing letters for blanks
            letters = list(word)
            #Checks if each blank letter provided is valid and if the number of letters provided by the user 
            # equal the amount of blank tiles played
            while True:
                try:
                    blank_letters = input(f"{player}, please enter your blank tile values in the order the appear in the word. No spaces between the letters: ")
                    for letter in blank_letters:
                        if not(letter.isalpha()):
                            raise InvalidInputError
                        else:
                            continue
                    break
                except InvalidInputError:
                    print(f"Word can only contain letters. Try again, {player}!", end="\n\n")
                    continue
            #adds the blank tile values (letters) to the word 
            try:
                for letter in word:
                    if letter == " ":
                        letters[word_count] = blank_letters[blank_count]
                        blank_count += 1
                    word_count += 1
                if len(blank_letters) == blank_count:
                    result_key = ''.join(letters)
                    result[result_key] = blank_letters
                    #Result is {'full word with blank values': 'blank letters used'}. This will allow keeping track of the correct score upon
                    # updating the score
                    print()
                    return result
                else:
                    raise IndexError
            except IndexError:
                print()
                print(f"Invalid number of blank tile values provided. Must equal the number of blank tiles used. Try again, {player}!", end="\n\n")
                continue
    #If there are no blanks, return the original word: "" (empty string for no blank values)
    else:
        print()
        result = {word: ""}
        return result

""" 
    Scores point total for the input word. Iterates through each letter 
    and adds score (value) of the letter (key) from dict 'letter_to_points'.
    Returns the point_total.
    Used by update_point_totals().
"""       
def score_word(word):
    point_total = 0
    for letter in word.upper():
        point_total += letter_to_points[letter]
    return point_total


"""
    Update the point totals for each player in player_to_points dict.

    Outter loop: 
        Iterates through each item of player_to_words dict.
        For each player (key), inner loop: 
            Iterates through each word from the word list (value) of each 
            item from the outer loop and adds to player_points. For each word,
            it subtracts the values of the letters used for blank tiles
        Updates player_points (value) for the player (key) in 
        player_to_points dict.
"""
def update_point_totals():
    for (player, words) in player_to_words.items():
        for word in words[-1].keys():
            #subtracts the values of the letters used for blank tiles
            player_points = (score_word(word) - words[-1][word])
        try:
            player_to_points[player] += player_points
        except KeyError:
            player_to_points.update({player: player_points})

"""
    Input scores for a round of scrabble.
    
    Loop through players list and call input_word() for each player. Once 
    done, call update_point_totals() to update the score, then display the 
    current score 
"""
def play_round():
    for player in players:
        play_word(player)
    print("Current score: ")
    update_point_totals()
    print(player_to_points, end="\n\n")
    another_round()

"""
    Calculate the winner and end the game.
"""    
def end_game():
    winners = []
    highest_score = 0
    """
    Loops through the items of player_to_points dict to calculate the
    highest score and associated player. Appends players who are tied and
    currently have the highest score to a list in case the highest score 
    is a tie.
    """
    for player, points in player_to_points.items():
        if points > highest_score:
            highest_score = points
            winners = [player]
        elif points == highest_score:
            winners.append(player)
    print()
    """
        Checks how many winners there are and prints the winner(s) to the
        console.
    """
    if len(winners) > 1 and player_to_points[winners[0]] == highest_score:
        print(f"It's a tie! ", end = "")
        if len(winners) == 2:
            print(f"{winners[0]} and {winners[1]} both win!! Thanks for playing!")
        elif len(winners) >= 2:
            winners_string = ""
            for winner in winners:
                if winners[-1] == winner:
                    winners_string += winner
                elif winners[-2] == winner:
                    winners_string += (winner + " and ")
                else:
                    winners_string += (winner + ", ")
            print(f"{winners_string} all win!! Thanks for playing")
    else:
        print(f"{winners[0]} wins!! Thanks for playing!")

"""
    Checks if the input provided by the user to play another round is
    correct. If not, raise an InvalidInputError exception
"""
def another_round():
    try:
        another_round_prompt = input("Would you like to play another round? ").lower()
        if another_round_prompt == "yes" or another_round_prompt == "y":
            print()
            play_round()
        elif another_round_prompt == "no" or another_round_prompt == "n":
            end_game()
            return
        else:
            raise InvalidInputError(another_round_prompt)
    except InvalidInputError:
        print()
        print("Please enter a valid response!", end = "\n\n")
        another_round()

def start_game():
    print()
    print("""############################""")
    print("""Welcome to Scrabble Scorer!!""")
    print("""############################""")
    print()

    #Populate players list
    get_players()

    #Welcome players to the game
    print()
    print("Welcome to the game ", end="") 
    print(*players, sep = ", ", end = "")
    print("!! Good luck!!")
    print()

    #Start first round
    play_round()


"""
##########
Start game
##########
"""
start_game()