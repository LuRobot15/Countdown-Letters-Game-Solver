import unittest
from unittest.mock import patch
from io import StringIO
from countdownSolver import solve_countdown, output_words
from createDict import initialise_dict

class TestCountdownSolver(unittest.TestCase):
	"""
	A test suite for the Countdown Solver functions.

	This class contains unit tests for the solve_countdown and output_words
	functions from the countdownSolver module.
	"""

	def setUp(self):
		"""
		Set up a sample dictionary for testing.

		This method is called before each test method. It initializes a sample
		dictionary that mimics the structure of the actual dictionary used in
		the Countdown Solver. This sample dictionary contains a few words with
		their definitions, counts, and letter counters.
		"""
		self.sample_dict = initialise_dict()
		self.sample_dict['a']['p'].append(
                    {"word": "apple", "definition": "A fruit", "count": 5, "letter_counter": {'a': 1, 'p': 2, 'l': 1, 'e': 1}},
		)
		self.sample_dict['a']['t'].append(
                    {"word": "at", "definition": "In, on, or near", "count": 2, "letter_counter": {'a': 1, 't': 1}},
		)
		self.sample_dict['t']['e'].append(
                    {"word": "test", "definition": "An examination", "count": 4, "letter_counter": {'t': 2, 'e': 1, 's': 1}},
		)
  
  
	def tearDown(self):
		"""
		Clean up the sample dictionary after each test.

		This method is called after each test method. It ensures that the sample
		dictionary is reset to its initial state after each test, maintaining
		consistency for subsequent tests.
		"""
		self.sample_dict = None


	def test_solve_countdown_valid_words(self):
		"""
		Test the solve_countdown function with valid words.

        This test case provides a set of letters that should match multiple words
        in the sample dictionary. It verifies that the solve_countdown function
        correctly identifies all valid words and returns them with their
        definitions and lengths.

        The test uses the letters "appletst", which should match "apple", "test",
        and "at" from the sample dictionary.

        Asserts:
            The result matches the expected list of word dictionaries, containing
            all valid words sorted by length in descending order.
        """
		letters = "appletst"
		result = solve_countdown(letters, self.sample_dict)
		expected = [
            {"word": "apple", "definition": "A fruit", "length": 5},
            {"word": "at", "definition": "In, on, or near", "length": 2},
            {"word": "test", "definition": "An examination", "length": 4},
        ]
		self.assertEqual(result, expected)


	def test_solve_countdown_no_valid_words(self):
		"""
		Test the solve_countdown function with no valid words.

        This test case provides a set of letters that should not match any words
        in the sample dictionary. It verifies that the solve_countdown function
        correctly returns an empty list when no valid words are found.

        The test uses the letters "xyz", which do not match any words in the
        sample dictionary.

        Asserts:
            The result is an empty list.
		"""
		letters = "xyz"
		result = solve_countdown(letters, self.sample_dict)
		self.assertEqual(result, [])


	def test_solve_countdown_partial_match(self):
		"""
		Test the solve_countdown function with partial word matches.

        This test case provides a set of letters that should match only some words
        in the sample dictionary. It verifies that the solve_countdown function
        correctly identifies partial matches and returns only the valid words.

        The test uses the letters "appl", which should only match "at" from the
        sample dictionary, as "apple" requires an additional 'e'.

        Asserts:
            The result matches the expected list containing only the partially
            matched word.
		"""
		letters = "applt"
		result = solve_countdown(letters, self.sample_dict)
		expected = [
            {"word": "at", "definition": "In, on, or near", "length": 2}
        ]
		self.assertEqual(result, expected)


	@patch('sys.stdout', new_callable=StringIO)
	def test_output_words(self, mock_stdout):
		"""
        Test the output_words function.

        This test case verifies that the output_words function correctly formats
        and prints the list of words to the console. It uses a mock stdout to
        capture the printed output and compare it with the expected string.

        The test provides a sample list of word dictionaries and checks if the
        output is formatted correctly, with words sorted by length in descending
        order.

        Args:
            mock_stdout (StringIO): A mock object to capture stdout.

        Asserts:
            The captured output matches the expected formatted string.
        """
		words = [
            {"word": "apple", "definition": "A fruit", "length": 5},
            {"word": "test", "definition": "An examination", "length": 4},
            {"word": "at", "definition": "In, on, or near", "length": 2}
		]
		output_words(words)
		expected_output = "5 - apple - A fruit\n4 - test - An examination\n2 - at - In, on, or near\n"
		self.assertEqual(mock_stdout.getvalue(), expected_output)


if __name__ == '__main__':
	unittest.main()
