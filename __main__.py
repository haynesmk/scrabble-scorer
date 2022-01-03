from scrabble_scorer import start_game, another_game

"""
    Main method
"""
def main():
    while True:
        start_game()
        if another_game() == True:
            continue
        else:
            break

if __name__ == "__main__":
    main()
