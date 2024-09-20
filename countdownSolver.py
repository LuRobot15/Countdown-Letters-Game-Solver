from collections import Counter
from typing import List

def solve_countdown(letters: str, search_dict: dict) -> List[dict]:
	"""
	Solve the Countdown numbers game using a dictionary and the provided letters. Ensuring no duplicate words are used.

	Args:
		letters (str): The letters provided for the game.
		search_dict (dict): The dictionary to search for valid words.

	Returns:
		list[dict]: A list of dictionaries containing the words, their definitions, and the word lengths.
	"""
	letter_counts = Counter(letters)
	valid_words = []
	letters_seen =[]

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
				word, definition, word_counts = record["word"], record["definition"], record["letter_counter"]
				if all(letter_counts[letter] >= count for letter, count in word_counts.items()):
					valid_words.append({"word": word, "definition": definition, "length": len(word)})

	return valid_words


def output_words(words: List[dict]) -> None:
	"""
	Output the words to the console.

	Args:
		words (list[dict]): A list of dictionaries containing the words, their definitions, and the word lengths.
	"""
	words.sort(key=lambda x: x["length"], reverse=True)

	for record in words:
		print(f'{record["length"]} - {record["word"]} - {record["definition"]}')

