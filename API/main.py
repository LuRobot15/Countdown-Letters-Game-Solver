from typing import Annotated

from fastapi import FastAPI, Query, HTTPException

from LettersGame.CountdownSolver import solve_countdown
from LettersGame.CreateDict import load_dict

app = FastAPI()

dict_path = "LettersGame/dict.json"
dict = load_dict(dict_path)
if dict is None:
    raise RuntimeError("Failed to load the dictionary")


@app.get("/")
async def root():
    return {"message": "This is the root of the letters game server"}


@app.get("/answers/get")
def get_answers(letters: Annotated[str, Query(
    description="The 9 letters you want to make words from. Can be upper or lower case",
    min_length=9,
    max_length=9
)]):

    validate_input_is_char_str(letters)
    usable_letters = letters.lower()
    results = solve_countdown(usable_letters, dict)
    results.sort(key=lambda x: x["length"], reverse=True)
    return results


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
