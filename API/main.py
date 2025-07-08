from typing import Annotated

from fastapi import FastAPI, Query, HTTPException

from LettersGame.CountdownSolver import solve_countdown, check_answer
from LettersGame.CreateDict import load_dict

app = FastAPI()

dict_path = "LettersGame/dict.json"
dict = load_dict(dict_path)
if dict is None:
    raise RuntimeError("Failed to load the dictionary")


@app.get("/")
async def root():
    return {"message": "This is the root of the letters game server"}


@app.get("/answers/get/")
def get_answers(
    letters: Annotated[
        str,
        Query(
            description="\
                The 9 letters you want to make words from. \
                    Can be upper or lower case",
            min_length=9,
            max_length=9
        )
    ]
):
    """
    Gets all the words in the dataset that can be formed
    from a subset of the letters in "letters"

    Args:
        letters (str): "The 9 letters you want to make words from.
                        Can be upper or lower case",
                        min_length=9,
                        max_length=9.

    Returns:
        dict:
            {
                "word": "the word",
                "definition": "the definition",
                "count": the length of the word,
            }
    """
    letters = preprocess_str_inp(letters)
    results = solve_countdown(letters, dict)
    results.sort(key=lambda x: x["length"], reverse=True)
    return results


@app.get("/answers/check/")
def check_answer_endpoint(
    letters: Annotated[
        str,
        Query(
            description="\
                The 9 letters you want to make words from. \
                    Can be upper or lower case",
            min_length=9,
            max_length=9
        )
    ],
    word: Annotated[
        str,
        Query(
            description="The word to check",
            min_length=3,
            max_length=9
        )
    ]
):
    """
    checks if the word if a valid answer to the letters game
    with those letters

    Args:
        letters (str): The 9 letters you want to make words from.
                        Can be upper or lower case.
                        min_length=9,
                        max_length=9.
        word (str): The word to check,
                    min_length=3,
                    max_length=9.

    Returns:
        dict: {
            "correct": (bool) True if the word exists and
                                contains only letters in "letters",
            "definitions": (List[str]) The definitions of the word,
                                        empty list if word invalid
        }
    """
    letters = preprocess_str_inp(letters)
    word = preprocess_str_inp(word)

    return check_answer(
        letters=letters,
        word=word,
        search_dict=dict
    )


def preprocess_str_inp(s: str) -> str:
    """
    Asserts a string is all letters
    Returns the str in lowercase

    Args:
        s (str): the input string

    Returns:
        str: the preprocessed string
    """
    validate_input_is_char_str(s)
    return s.lower()


def validate_input_is_char_str(s: str) -> None:
    """
    Asserts a string contains only letters,
    raising a HTTPException if not

    Args:
        s (str): The input string

    Raises:
        HTTPException: terminates the request and
                       informs the client of their error
    """
    if not s.isalpha():
        raise HTTPException(
            status_code=400,
            detail="letters must contain letters only"
        )
