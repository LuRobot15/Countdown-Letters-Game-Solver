from collections import Counter

def solve_countdown(letters: str, search_dict: dict) -> list[dict]:
	"""
	Solve the Countdown numbers game using a dictionary and the provided letters.

	Args:
		letters (str): The letters provided for the game.
		search_dict (dict): The dictionary to search for valid words.

	Returns:
		list[dict]: A list of dictionaries containing the words, their definitions, and the word lengths.
	"""
	letter_counts = Counter(letters)
	valid_words = []

	for i in range(len(letters)):
		for j in range(len(letters)):
			if i == j:
				continue
			
			for record in search_dict[i][j]:
				word = record["word"]
				definition = record["definition"]
				word_counts = record["letter_counter"]
				if all(letter_counts[letter] >= count for letter, count in word_counts.items()):
					valid_words.append({"word": word, "definition": definition, "length": len(word)})

	return valid_words


def output_words(words: list[dict]) -> None:
	"""
	Output the words to the console.

	Args:
		words (list[dict]): A list of dictionaries containing the words, their definitions, and the word lengths.
	"""
	words.sort(key=lambda x: x["length"], reverse=True)

	for record in words:
		print(f'{record["length"]} - {record["word"]} - {record["definition"]}')

