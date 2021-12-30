import enchant
import os

"""
    Class that defines InvalidInputError exception
"""
class InvalidInputError(Exception):
    """
        Exception raised for invalid input provided by user
    """
    def __init__(self, message="Please provide a valid input"):
        self.message = message
        super().__init__(self.message)

class InvalidWordError(Exception):
    """
        Exception raised for invalid word provided by user
    """
    def __init__(self, message="Please provide a real word"):
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
    in player_to_words dict
"""
def play_word(player):
    try:
        word = input(f"{player}'s turn. Please input a word: ")
        if spellcheck.check(word) == True:
            try:
                player_to_words[player].append(word)
            except KeyError:
                player_to_words[player] = []
                player_to_words[player].append(word)
        else:
            raise InvalidWordError
    except InvalidWordError:
        print()
        print(f"Invalid word! Must be a valid word from the English dictionary. Try again, {player}.", end="\n\n")
        play_word(player)
    except ValueError:
        print(f"String can't be empty!  Try again, {player}.", end="\n\n")
        play_word(player)

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
            item from the outer loop and adds to player_points. 
        Updates player_points (value) for the player (key) in 
        player_to_points dict.
"""
def update_point_totals():
    for player, words in player_to_words.items():
        player_points = 0
        for word in words:
            player_points += score_word(word)
        try:
            player_to_points[player] = player_points
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
    print()
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
            print("both win!! Thanks for playing!")
        elif len(winners) >= 2:
            print("all win!! Thanks for playing")
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
    print("""############################
Welcome to Scrabble Scorer!!
############################
""")

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