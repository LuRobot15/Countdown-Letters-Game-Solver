from createDict import create_dict, load_dict

def main(args: list):
	"""
	Main function to handle user input and perform actions based on the choice.

	Args:
		args (list): List of command-line arguments.

	Returns:
		None
	"""
	if len(args) != 0:
		print("Usage: python main.py")
		return

	choice = 0
	search_dictionary = None

	while choice != -1:
		print("What would you like to do?")
		print("1. create dict")
		print("2. Load dict")
		print("3. Exit")

		choice = input("Enter your choice: ")

		match choice:
			case "1":
				search_dictionary = command_create_dict()
			case "2":
				search_dictionary = command_load_dict()
			case "-1":
				break
			case _:
				print("Invalid choice")


def command_create_dict() -> dict | None:
	"""
	Create a dictionary and store it in a file from files given by the user.

	Args:
		
	Returns:
		dict | None: The dictionary if created successfully, None otherwise.
	"""
	data_csv = input("Enter the path to the csv file containing the words: ")
	dict_json = input("Enter the path to the json file to store the dictionary: ")

	search_dictionary = create_dict(data_csv, dict_json)

	if search_dictionary is None:
		print("Error: Failed to create dictionary")
	else:
		print("Dictionary created successfully")

	return search_dictionary


def command_load_dict() -> dict | None:
	"""
	Load a dictionary from a json file.

	Args:
		None
	Returns:
		dict | None: The dictionary if loaded successfully, None otherwise.
	"""
	dict_json = input("Enter the path to the json file to load the dictionary: ")

	search_dictionary = load_dict(dict_json)

	if search_dictionary is None:
		print("Error: Failed to load dictionary")
	else:
		print("Dictionary loaded successfully")

	return search_dictionary




		