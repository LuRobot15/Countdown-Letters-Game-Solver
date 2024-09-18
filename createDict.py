import csv
import string
from collections import Counter
import json
from typing import Union

"""
The structure of the dictionary is as follows:

{
    "first letter of word": {
        "second letter of word": [
            {
                "word": "the word",
                "definition": "the definition",
                "count": the length of the word,
                "letter_counter": a counter of the letters in the word
            },
        ]
    }
}
"""

def create_dict(csv_file_path: str, file_path: str) -> Union[dict, None]:
	"""
	Create a dict object that stores all valid answers to a possible countdown letters game from a CSV file.
    
	Args:
		csv_file_path (str): The path to the CSV file.
        file_path (str): The path to the file to store the dictionary.
	Returns:
    	dictionary (dict): A dictionary with first letters of words as keys and dictionary with second letters of words as values.
	"""
	try:
		with open(csv_file_path, 'r') as file:
			dictionary = initialise_dict()

		csv_reader = csv.reader(file)
		for row in csv_reader:
			word, definition = row[0], row[3]
   
			if '\'' in word or ' ' in word or '-' in word:
				continue
			else:
				add_to_dict(dictionary, word, definition)
	except Exception as e:
		print(f"Error: {e}")
		return None

	store_dict(dictionary, file_path)
	return dictionary


def initialise_dict() -> dict:
	"""
	Initialise a dictionary with all possible first letters of words with a dictionary of all possible letters as values, the second dictionary will have an empty list as values.

	Returns:
		dictionary (dict): A dictionary with all possible first letters of words with a dictionary of all possible letters as values, the second dictionary will have an empty list as values.
	"""
	dictionary = {}
	for first_letter in string.ascii_lowercase:
		dictionary[first_letter] = {}
		for second_letter in string.ascii_lowercase:
			dictionary[first_letter][second_letter] = []

	return dictionary


def add_to_dict(dictionary: dict, word: str, definition: str) -> None:
	"""
	Add a word, its definition, count and counter of letters to the dictionary.

	Args:
		dictionary (dict): The dictionary to add to.
		word (str): the word to add
		definition (str): the words definition
	"""
	letter_counter = Counter(word)
	dictionary[word[0]][word[1]].append({
     "word" : word,
     "definition" : definition,
     "count" : len(word),
     "letter_counter" : letter_counter
     })


def store_dict(dictionary: dict, file_path: str) -> None:
	"""
	Store the dictionary to a file in JSON format.

	Args:
		dictionary (dict): The dictionary to store.
		file_path (str): The path to the file to store the dictionary.
	"""
	with open(file_path, 'w') as file:
		json.dump(dictionary, file)
  
  
def load_dict(file_path: str) -> Union[dict, None]:
	"""
	Load the dictionary from a file in JSON format.

	Args:
		file_path (str): The path to the file to load the dictionary from.

	Returns:
		dictionary (dict): The dictionary loaded from the file.
	"""
	try:
		with open(file_path, 'r') as file:
			dictionary = json.load(file)

		return dictionary
	except Exception as e:
		print(f"Error: {e}")
		return None






    






