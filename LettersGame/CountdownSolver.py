from collections import Counter
from typing import List


def solve_countdown(letters: str, search_dict: dict) -> List[dict]:
    """
    Solve the Countdown numbers game using a dictionary and
    the provided letters. Ensuring no duplicate words are used.

    Args:
        letters (str): The letters provided for the game.
        search_dict (dict): The dictionary to search for valid words.

    Returns:
        list[dict]: A list of dictionaries containing the words,
                    their definitions, and the word lengths.
    """
    letter_counts = Counter(letters)
    valid_words = []
    letters_seen = []

    for i in range(len(letters)):
        if letters[i] in letters_seen:
            continue
        letters_seen.append(letters[i])

        second_letters_seen = []
        for j in range(len(letters)):
            if i == j or letters[j] in second_letters_seen:
                continue
            second_letters_seen.append(letters[j])

            for record in search_dict[letters[i]][letters[j]]:
                if check_word(letter_counts, record["letter_counter"]):
                    valid_words.append({
                        "word": record["word"],
                        "definition": record["definition"],
                        "length": len(record["word"])
                        })

    return valid_words


def check_word(
    letter_counts: dict,
    word_counts: dict,
) -> bool:
    """
    checks if a word can be formed from the letters given

    Args:
        letter_counts (dict): The letters available
        word_counts (dict): The counter for the word

    Returns:
        bool: True if "word_counts" is a subset of "letter_counts"
    """
    if all(
        letter_counts[letter] >= count for letter, count in word_counts.items()
    ):
        return True
    return False


def output_words(words: List[dict]) -> None:
    """
    Output the words to the console.

    Args:
        words (list[dict]): A list of dictionaries containing the words,
                            their definitions, and the word lengths.
    """
    words.sort(key=lambda x: x["length"], reverse=True)

    for record in words:
        print(
            f'{record["length"]} - {record["word"]} - {record["definition"]}'
            )


def check_answer(word: str, letters: str, search_dict: dict) -> dict:
    """
    checks if the word can be formed from a subset of 'letters'
    checks if  the word is in the dict
    returns the definition

    Args:
        word (str): The word submitted
        letters (str): The available letters
        search_dict (dict): the search dict to search for words

    Returns:
        dict: The return dict
                {
                    correct: (bool) if the word is correct
                    definitions: (list[string]) the definitions of the word
                }
    """
    return_dict = {
        "correct": False,
        "definitions": []
    }

    word_counter = Counter(word)
    letters_counter = Counter(letters)

    for key in word_counter:
        if (
            key not in letters_counter or
            word_counter[key] > letters_counter[key]
        ):
            return return_dict

    same_opening_words = search_dict[word[0]][word[1]]
    for word_dict in same_opening_words:
        if word_dict["word"] == word:
            return_dict["correct"] = True
            return_dict["definitions"].append(word_dict["definition"])

    return return_dict
