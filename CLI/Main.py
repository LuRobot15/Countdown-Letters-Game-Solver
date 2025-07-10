from LettersGame.CreateDict import create_dict, load_dict
from LettersGame.CountdownSolver import (
    solve_countdown,
    output_words,
    check_answer
)
from typing import Union, List
import random

VOWLS = "aeiou"
CONSONANTS = "bcdfghjklmnpqrstvwxyz"


def main(args: list):
    """
    Main function to handle user input and perform actions based on the choice.

    Args:
        args (list): List of command-line arguments.

    Returns:
        None
    """
    if len(args) != 1:
        print("Usage: python main.py")
        return

    choice = 0
    search_dictionary = None

    while choice != -1:
        print("What would you like to do?")
        print("1. create dict")
        print("2. Load dict")
        print("3. Solve Countdown")
        print("-1. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            search_dictionary = command_create_dict()
        elif choice == "2":
            search_dictionary = command_load_dict()
        elif choice == "3" and search_dictionary is not None:
            command_solve_countdown(search_dictionary)
        elif choice == "4" and search_dictionary is not None:
            command_play_game(search_dictionary)
        elif choice == "-1":
            break
        elif choice == "3" or choice == "4":
            print("You must load a dictionary first")
        else:
            print("Invalid choice")


def command_create_dict() -> Union[dict, None]:
    """
    Create a dictionary and store it in a file from files given by the user.

    Args:

    Returns:
        dict | None: The dictionary if created successfully, None otherwise.
    """
    data_csv = input(
        "Enter the path to the csv file containing the words: "
        )
    dict_json = input(
        "Enter the path to the json file to store the dictionary: "
        )

    search_dictionary = create_dict(data_csv, dict_json)

    if search_dictionary is None:
        print("Error: Failed to create dictionary")
    else:
        print("Dictionary created successfully")

    return search_dictionary


def command_load_dict() -> Union[dict, None]:
    """
    Load a dictionary from a json file.

    Args:
        None
    Returns:
        dict | None: The dictionary if loaded successfully, None otherwise.
    """
    dict_json = input(
        "Enter the path to the json file to load the dictionary: "
        )

    search_dictionary = load_dict(dict_json)

    if search_dictionary is None:
        print("Error: Failed to load dictionary")
    else:
        print("Dictionary loaded successfully")

    return search_dictionary


def command_solve_countdown(search_dictionary: dict) -> None:
    """
    Solve the countdown problem for a given set of letters.

    Args:
        search_dictionary (dict): The dictionary to use to find words.
    """
    letters = manually_enter_letters()

    if letters is None:
        return

    valid_words = solve_countdown(letters.lower(), search_dictionary)

    output_words(valid_words)

    if valid_words is None:
        print("Error: Failed to solve countdown problem")
    else:
        print("Countdown problem solved successfully")


def command_play_game(search_dictionary: dict) -> None:
    """
    Allow a user to play the countdown game by entering words which are checked

    Args:
        search_dictionary (dict): The search dictionary storing words
    """
    letter_draw_choice = "0"
    letters = ""
    while (
        (
            letter_draw_choice != "1" and letter_draw_choice != "2"
        ) or
        letters == "-1"
    ):
        print("Would you like to manually type your letter pool, or draw it?")
        print("1. Manually type letters")
        print("2. Draw letters (Real Countdown)")
        print("-1. Return")
        letter_draw_choice = input("Enter your choice: ")

        if letter_draw_choice == "1":
            letters = manually_enter_letters()
        elif letter_draw_choice == "2":
            letters = draw_letters()
        elif letter_draw_choice == "-1":
            return

    if letters is None:
        return

    guess = ""
    while guess != "-1":
        print(f"letters: {letters}")
        guess = input("input a word (or -1 to see answers): ")
        if len(guess) > 9 or not guess.isalpha():
            print("Invalid Guess")
            guess = ""
        else:
            response = check_answer(guess, letters, search_dictionary)
            if not response["correct"]:
                print("incorrect")
            else:
                print("correct")
        guess = ""

    valid_words = solve_countdown(letters, search_dictionary)
    output_words(valid_words)


def output_definitions(definitions: List[str]) -> None:
    """
    Outputs the difinitions of the word

    Args:
        definitions (List[str]): The list of definitions
    """
    print("Word Definitions:")
    for i in range(len(definitions)):
        print(f"{i}. {definitions[i]}")


def manually_enter_letters() -> Union[str, None]:
    """
    Allows a user to manually enter letters,
    processing them to ensure they are correct

    Returns:
        str: valid letter pool
    """
    letters = ""

    while True:
        letters = input("Enter letters (or -1 to exit): ")
        if letters == "-1":
            return None
        if len(letters) != 9 or not letters.isalpha():
            print("Error: Invalid Input, must be 9 letters")
        else:
            letters = letters.lower()
            return letters


def draw_letters() -> Union[str, None]:
    """
    Creates a string of 9 letters from which to play the game
    Either by manual choice or by drawing letters randomly

    Returns:
        str: the letters to play the game with
    """
    print("You will be asked for your choice of:")
    print(f"v: vowl ({VOWLS})")
    print("c: consonants (the rest of the letters)")
    print("A letter from that catagory will be randomly selected " +
          "and added to the pool")
    print("This will be repeated until a pool of 9 letters is created")
    print("Thest letters will be used to play the game")

    letters = ""
    while len(letters) < 9:
        letter_choice = input(
            "What letter type would you like? (v) or (c)"
            )

        if letter_choice == "c":
            new_letter = select_letter(CONSONANTS)
        elif letter_choice == "v":
            new_letter = select_letter(VOWLS)
        elif letter_choice == "-1":
            return None
        else:
            new_letter = ""

        letters = letters + new_letter

        print(letters)

    return letters


def select_letter(pool: str) -> str:
    """randomly draws a letter from a string

    Args:
        pool (str): the pool of letters to select from

    Returns:
        str: the selected letter
    """
    return random.choice(pool)
