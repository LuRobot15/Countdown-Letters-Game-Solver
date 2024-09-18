import unittest
from unittest.mock import patch, MagicMock
from io import StringIO
import sys
from main import main, command_create_dict, command_load_dict

class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=['1', '-1'])
    @patch('main.command_create_dict')
    def test_main_create_dict(self, mock_create_dict, mock_input):
        """
        Test the main function when the user chooses to create a dictionary.

        This test simulates user input to select the option to create a dictionary
        and then exit the program. It verifies that the appropriate functions are
        called and the expected output is produced.

        Args:
            mock_create_dict (MagicMock): Mocked command_create_dict function.
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The output contains the prompt "What would you like to do?".
            The command_create_dict function is called once.
        """
        mock_create_dict.return_value = {'test': 'dictionary'}
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main([])
        self.assertIn("What would you like to do?", fake_out.getvalue())
        mock_create_dict.assert_called_once()


    @patch('builtins.input', side_effect=['2', '-1'])
    @patch('main.command_load_dict')
    def test_main_load_dict(self, mock_load_dict, mock_input):
        """
        Test the main function when the user chooses to load a dictionary.

        This test simulates user input to select the option to load a dictionary
        and then exit the program. It verifies that the appropriate functions are
        called and the expected output is produced.

        Args:
            mock_load_dict (MagicMock): Mocked command_load_dict function.
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The output contains the prompt "What would you like to do?".
            The command_load_dict function is called once.
        """
        mock_load_dict.return_value = {'test': 'dictionary'}
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main([])
        self.assertIn("What would you like to do?", fake_out.getvalue())
        mock_load_dict.assert_called_once()


    @patch('builtins.input', side_effect=['3', '-1'])
    def test_main_invalid_choice(self, mock_input):
        """
        Test the main function when the user chooses an invalid option.

        This test simulates user input to select an invalid option and then exit the program.
        It verifies that the appropriate message is displayed.

        Args:
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The output contains the prompt "Invalid choice".
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main([])
        self.assertIn("Invalid choice", fake_out.getvalue())


    @patch('builtins.input', side_effect=['/path/to/csv', '/path/to/json'])
    @patch('main.create_dict')
    def test_command_create_dict_success(self, mock_create_dict, mock_input):
        """
        Test the command_create_dict function when the dictionary is created successfully.

        This test simulates user input for the CSV and JSON file paths and mocks the create_dict
        function to return a test dictionary. It verifies that the function returns the expected
        dictionary and the appropriate success message is displayed.

        Args:
            mock_create_dict (MagicMock): Mocked create_dict function.
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The result is the test dictionary.
            The output contains the message "Dictionary created successfully".
        """
        mock_create_dict.return_value = {'test': 'dictionary'}
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = command_create_dict()
        self.assertEqual(result, {'test': 'dictionary'})
        self.assertIn("Dictionary created successfully", fake_out.getvalue())


    @patch('builtins.input', side_effect=['/path/to/csv', '/path/to/json'])
    @patch('main.create_dict')
    def test_command_create_dict_failure(self, mock_create_dict, mock_input):
        mock_create_dict.return_value = None
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = command_create_dict()
        self.assertIsNone(result)
        self.assertIn("Error: Failed to create dictionary", fake_out.getvalue())


    @patch('builtins.input', return_value='/path/to/json')
    @patch('main.load_dict')
    def test_command_load_dict_success(self, mock_load_dict, mock_input):
        """
        Test the command_load_dict function when the dictionary is loaded successfully.

        This test simulates user input for the JSON file path and mocks the load_dict
        function to return a test dictionary. It verifies that the function returns the expected
        dictionary and the appropriate success message is displayed.

        Args:
            mock_load_dict (MagicMock): Mocked load_dict function.
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The result is the test dictionary.
            The output contains the message "Dictionary loaded successfully".
        """
        mock_load_dict.return_value = {'test': 'dictionary'}
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = command_load_dict()
        self.assertEqual(result, {'test': 'dictionary'})
        self.assertIn("Dictionary loaded successfully", fake_out.getvalue())


    @patch('builtins.input', return_value='/path/to/json')
    @patch('main.load_dict')
    def test_command_load_dict_failure(self, mock_load_dict, mock_input):
        """
        Test the command_load_dict function when the dictionary fails to load.

        This test simulates user input for the JSON file path and mocks the load_dict
        function to return None. It verifies that the function returns None and the 
        appropriate error message is displayed.

        Args:
            mock_load_dict (MagicMock): Mocked load_dict function.
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The result is None.
            The output contains the message "Error: Failed to load dictionary".
        """
        mock_load_dict.return_value = None
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = command_load_dict()
        self.assertIsNone(result)
        self.assertIn("Error: Failed to load dictionary", fake_out.getvalue())


if __name__ == '__main__':
    unittest.main()
