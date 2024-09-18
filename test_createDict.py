import unittest
import os
import json
from createDict import create_dict, initialise_dict, add_to_dict, store_dict
from collections import Counter

class TestCreateDict(unittest.TestCase):
    """
    Test suite for the createDict module functions.
    """

    def setUp(self):
        """
        Set up the test environment before each test method.
        Creates a temporary CSV file with test data.
        """
        # Create a temporary CSV file for testing
        self.test_csv_path = 'test_words.csv'
        with open(self.test_csv_path, 'w') as f:
            f.write('apple,5,noun,a fruit\n')
            f.write('banana,6,noun,a yellow fruit\n')
            f.write('cat,3,noun,a feline animal\n')
            f.write("don't,5,verb,contraction of do not\n")  # This should be skipped

    def tearDown(self):
        """
        Clean up the test environment after each test method.
        Removes temporary files created during testing.
        """
        # Remove the temporary CSV file
        os.remove(self.test_csv_path)
        if os.path.exists('test_dictionary.txt'):
            os.remove('test_dictionary.txt')

    def test_create_dict(self):
        """
        Test the create_dict function.
        
        Verifies that:
        1. The dictionary is created with the correct structure.
        2. Words are properly added to the dictionary.
        3. Words with apostrophes are skipped.
        """
        result = create_dict(self.test_csv_path, 'test_dictionary.txt')
        self.assertIn('a', result)
        self.assertIn('b', result)
        self.assertIn('c', result)
        self.assertEqual(len(result['a']['p']), 1)
        self.assertEqual(len(result['b']['a']), 1)
        self.assertEqual(len(result['c']['a']), 1)
        self.assertEqual(len(result['d']['o']), 0)

    def test_initialise_dict(self):
        """
        Test the initialise_dict function.
        
        Verifies that:
        1. The dictionary is initialized with 26 first-level keys (a-z).
        2. Each first-level key contains 26 second-level keys (a-z).
        3. All second-level keys have empty lists as values.
        """
        result = initialise_dict()
        self.assertEqual(len(result), 26)
        for first_letter in result:
            self.assertEqual(len(result[first_letter]), 26)
            for second_letter in result[first_letter]:
                self.assertEqual(result[first_letter][second_letter], [])

    def test_add_to_dict(self):
        """
        Test the add_to_dict function.
        
        Verifies that:
        1. A word is correctly added to the dictionary.
        2. The word entry contains the correct word, definition, count, and letter counter.
        """
        dictionary = initialise_dict()
        add_to_dict(dictionary, 'test', 'a trial')
        self.assertEqual(len(dictionary['t']['e']), 1)
        entry = dictionary['t']['e'][0]
        self.assertEqual(entry['word'], 'test')
        self.assertEqual(entry['definition'], 'a trial')
        self.assertEqual(entry['count'], 4)
        self.assertEqual(entry['letter_counter'], Counter('test'))

    def test_store_dict(self):
        """
        Test the store_dict function.
        
        Verifies that:
        1. The dictionary is correctly stored in a JSON file.
        2. The stored dictionary can be loaded and matches the original dictionary.
        """
        dictionary = {'a': {'b': [{'word': 'ab', 'definition': 'test', 'count': 2, 'letter_counter': Counter('ab')}]}}
        store_dict(dictionary, 'test_dictionary.txt')
        self.assertTrue(os.path.exists('test_dictionary.txt'))
        with open('test_dictionary.txt', 'r') as f:
            stored_dict = json.load(f)
        self.assertEqual(stored_dict, dictionary)

if __name__ == '__main__':
    unittest.main()
