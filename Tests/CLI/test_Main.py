from collections import Counter
import unittest
from unittest.mock import call, patch, MagicMock
from io import StringIO
from CLI.Main import (
    main,
    command_create_dict,
    command_load_dict,
    command_solve_countdown,
    command_play_game,
    play_game_letter_generation,
    manually_enter_letters,
    draw_letters
)
from LettersGame.CountdownSolver import (
    check_answer,
    solve_countdown,
    output_words
)


class TestMain(unittest.TestCase):

    @patch('builtins.input', side_effect=['1', '-1'])
    @patch('CLI.Main.command_create_dict')
    def test_main_create_dict(self, mock_create_dict, mock_input):
        """
        Test the main function when the user chooses to create a dictionary.

        This test simulates user input to select the option to
        create a dictionary and then exit the program. It verifies that
        the appropriate functions are called and the expected output
        is produced.

        Args:
            mock_create_dict (MagicMock): Mocked command_create_dict function.
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The output contains the prompt "What would you like to do?".
            The command_create_dict function is called once.
        """
        mock_create_dict.return_value = {'test': 'dictionary'}
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(["main.py"])
        self.assertIn("What would you like to do?", fake_out.getvalue())
        mock_create_dict.assert_called_once()

    @patch('builtins.input', side_effect=['2', '-1'])
    @patch('CLI.Main.command_load_dict')
    def test_main_load_dict(self, mock_load_dict, mock_input):
        """
        Test the main function when the user chooses to load a dictionary.

        This test simulates user input to select the option to
        load a dictionary and then exit the program. It verifies that
        the appropriate functions are called and the expected output
        is produced.

        Args:
            mock_load_dict (MagicMock): Mocked command_load_dict function.
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The output contains the prompt "What would you like to do?".
            The command_load_dict function is called once.
        """
        mock_load_dict.return_value = {'test': 'dictionary'}
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(["main.py"])
        self.assertIn("What would you like to do?", fake_out.getvalue())
        mock_load_dict.assert_called_once()

    @patch('builtins.input', side_effect=['2', '3', '-1'])
    @patch('CLI.Main.command_solve_countdown')
    @patch('CLI.Main.command_load_dict')
    def test_main_solve_countdown(
        self,
        mock_command_load_dict,
        mock_command_solve_countdown,
        mock_input
    ):
        """
        Test the main function for when the user chooses to solve
        the countdown problem.

        This test simulates user input to select the option to solve the
        countdown problem and then exit the program. It verifies that the
        appropriate functions are called and the expected output is produced.

        Args:
            mock_command_solve_countdown (MagicMock): Mocked
                    command_solve_countdown function.

            mock_input (MagicMock): Mocked input function.

        Asserts:
            The output contains the prompt "What would you like to do?".
            The command_solve_countdown function is called once.
        """
        mock_dict = {'test': 'dictionary'}
        mock_command_load_dict.return_value = mock_dict
        mock_command_solve_countdown.return_value = None
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(["main.py"])
        self.assertIn("What would you like to do?", fake_out.getvalue())
        mock_command_solve_countdown.assert_called_once_with(mock_dict)

    @patch('builtins.input', side_effect=['2', '4', '-1'])
    @patch('CLI.Main.command_play_game')
    @patch('CLI.Main.command_load_dict')
    def test_main_play_game(
        self,
        mock_command_load_dict: MagicMock,
        mock_command_play_game: MagicMock,
        mock_input: MagicMock
    ):
        """
        Test the main function for when the user chooses to play
        the countdown game.

        This test simulates user input to select the option to play the
        countdown game and then exit the program. It verifies that the
        appropriate functions are called and the expected output is produced.

        Args:
            mock_command_load_dict (MagicMock): The mocked load dict function
            mock_command_play_game (MagicMock): The mocked play game function
            mock_input (MagicMock): The mocked input selecting the options

        Asserts:
            The output contains the prompt "What would you like to do?".
            The command_play_game function is called once.
        """
        mock_dict = {'test': 'dictionary'}
        mock_command_load_dict.return_value = mock_dict
        mock_command_play_game.return_value = None
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(["main.py"])
        self.assertIn("What would you like to do?", fake_out.getvalue())
        mock_command_play_game.assert_called_once_with(mock_dict)

    @patch('builtins.input', side_effect=['5', '-1'])
    def test_main_invalid_choice(self, mock_input):
        """
        Test the main function when the user chooses an invalid option.

        This test simulates user input to select an invalid option and then
        exit the program.
        It verifies that the appropriate message is displayed.

        Args:
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The output contains the prompt "Invalid choice".
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(["main.py"])
        self.assertIn("Invalid choice", fake_out.getvalue())

    @patch('builtins.input', side_effect=['3', '-1'])
    def test_solve_without_dict(self, mock_input):
        """
        Test the main function when the user chooses an invalid option.

        This test simulates user input to select to solve countdown
        without first loading a dictionary and then exits the program.
        It verifies that the appropriate message is displayed.

        Args:
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The output contains the prompt "You must load a dictionary first".
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(["main.py"])
        self.assertIn("You must load a dictionary first", fake_out.getvalue())

    @patch('builtins.input', side_effect=['4', '-1'])
    def test_play_game_without_dict(self, mock_input):
        """
        Test the main function when the user chooses an invalid option.

        This test simulates user input to selects to play the game
        without first loading a dictionary and then exits the program.
        It verifies that the appropriate message is displayed.

        Args:
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The output contains the prompt "You must load a dictionary first".
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main(["main.py"])
        self.assertIn("You must load a dictionary first", fake_out.getvalue())

    @patch('builtins.input', side_effect=['/path/to/csv', '/path/to/json'])
    @patch('CLI.Main.create_dict')
    def test_command_create_dict_success(self, mock_create_dict, mock_input):
        """
        Test the command_create_dict function when the dictionary is created
        successfully.

        This test simulates user input for the CSV and JSON file paths and
        mocks the create_dict function to return a test dictionary.
        It verifies that the function returns the expected dictionary and the
        appropriate success message is displayed.

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
    @patch('CLI.Main.create_dict')
    def test_command_create_dict_failure(self, mock_create_dict, mock_input):
        mock_create_dict.return_value = None
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = command_create_dict()
        self.assertIsNone(result)
        self.assertIn(
            "Error: Failed to create dictionary", fake_out.getvalue()
        )

    @patch('builtins.input', return_value='/path/to/json')
    @patch('CLI.Main.load_dict')
    def test_command_load_dict_success(self, mock_load_dict, mock_input):
        """
        Test the command_load_dict function when the dictionary is loaded
        successfully.

        This test simulates user input for the JSON file path and mocks the
        load_dict function to return a test dictionary.
        It verifies that the function returns the expected dictionary and the
        appropriate success message is displayed.

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
    @patch('CLI.Main.load_dict')
    def test_command_load_dict_failure(self, mock_load_dict, mock_input):
        """
        Test the command_load_dict function when the dictionary fails to load.

        This test simulates user input for the JSON file path and mocks the
        load_dict function to return None.
        It verifies that the function returns None and the appropriate error
        message is displayed.

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

    @patch('builtins.input', return_value='ABCDEFGHI')
    @patch('CLI.Main.solve_countdown')
    @patch('CLI.Main.output_words')
    def test_command_solve_countdown_success(
        self,
        mock_output_words,
        mock_solve_countdown,
        mock_input
    ):
        """
        Test the command_solve_countdown function when the countdown is solved
        successfully.

        This test simulates user input for the letters and mocks the
        solve_countdown and output_words functions. It verifies that the
        appropriate functions are called and the expected output is produced.

        Args:
            mock_output_words (MagicMock): Mocked output_words function.
            mock_solve_countdown (MagicMock): Mocked solve_countdown function.
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The solve_countdown function is called with the correct arguments.
            The output_words function is called with the correct arguments.
            The output contains the message:
                "Countdown problem solved successfully".
        """
        mock_dict = {'test': 'dictionary'}
        mock_solve_countdown.return_value = [
            {
                'word': 'abc',
                'definition': 'test'
            }
        ]

        with patch('sys.stdout', new=StringIO()) as fake_out:
            command_solve_countdown(mock_dict)

        mock_solve_countdown.assert_called_once_with('abcdefghi', mock_dict)

        mock_output_words.assert_called_once_with([
            {
                'word': 'abc',
                'definition': 'test'
            }
        ])

        self.assertIn(
            "Countdown problem solved successfully", fake_out.getvalue()
        )

    @patch('builtins.input', side_effect=['INVALID', "-1"])
    def test_command_solve_countdown_invalid_input(self, mock_input):
        """
        Test the command_solve_countdown function when invalid input is
        provided.

        This test simulates user input with an invalid number of letters.
        It verifies that the appropriate error message is displayed.

        Args:
            mock_input (MagicMock): Mocked input function.

        Asserts:
            The output contains the message "Error: Invalid number of letters".
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            command_solve_countdown({})

        self.assertIn(
            "Error: Invalid Input, must be 9 letters", fake_out.getvalue()
        )

    @patch('builtins.input', side_effect=[
        'v', 'a', 'c', 'v', 'd', 'c', 'v', 'c', 'c', 'c', 'c'
        ]
    )
    def test_valid_draw_letters(self, mock_input):
        """
        Tests the draw letters function

        Simulates the use of the draw letters function.
        In the end, only 9 letters should appear with only
        3 being vowels

        Args:
            mock_input (MagicMock): The Mocked input

        Asserts:
            a 9 letter string is returned containing letters only with 3
            vowels and 6 consonents
        """
        with patch('sys.stdout', new=StringIO()):
            returned_letters = draw_letters()

        self.assertIsNotNone(returned_letters)
        self.assertEqual(len(returned_letters), 9)
        self.assertTrue(returned_letters.isalpha())
        self.assertTrue(returned_letters.islower())

        vowels = 'aeiou'
        letter_counter = Counter(returned_letters)
        total_vowels = 0
        for char in vowels:
            if char in letter_counter:
                total_vowels += letter_counter[char]

        self.assertEqual(total_vowels, 3)

    @patch('builtins.input', side_effect=[
        'v', 'a', 'c', 'v', 'd', 'c', 'v', 'c', 'c', 'c', '-1'
        ]
    )
    def test_draw_letters_ecit(self, mock_input):
        """
        Tests the draw letters function where the user exits before 9
        letters have been drawn

        Simulates the use of the draw letters function.
        In the end, None should be returned as the user has exitted before
        9 letters have been drawn

        Args:
            mock_input (MagicMock): The Mocked input

        Asserts:
            None is returned
        """
        with patch('sys.stdout', new=StringIO()):
            returned_letters = draw_letters()

        self.assertIsNone(returned_letters)

    @patch('builtins.input', return_value='aaaAaaAaa')
    def test_valid_manually_enter_letters(self, mock_input):
        """
        Tests the function to manually enter letters when a valid input is
        given

        Args:
            mock_input (MagicMock): The Mocked input

        Asserts:
            The 9 letters inputted are returned exactly
        """
        with patch('sys.stdout', new=StringIO()):
            returned_letters = manually_enter_letters()

        self.assertEqual(returned_letters, 'aaaaaaaaa')

    @patch('builtins.input', return_value='-1')
    def test_manually_enter_letters_abort(self, mock_input):
        """
        Tests the function to manually enter letters when the user exits

        Args:
            mock_input (MagicMock): The Mocked input

        Asserts:
            None is returned
        """
        with patch('sys.stdout', new=StringIO()):
            returned_letters = manually_enter_letters()

        self.assertIsNone(returned_letters)

    @patch('builtins.input', side_effect=['aaaaaaaa', '-1'])
    def test_manually_enter_letters_too_short(self, mock_input):
        """
        Tests the user is not allowed to enter a string that is too short

        Args:
            mock_input (MagicMock): The mocked input

        Asserts:
            The correct error message is shown and None is returned
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            returned_letters = manually_enter_letters()

        self.assertIn(
            "Error: Invalid Input, must be 9 letters", fake_out.getvalue()
        )
        self.assertIsNone(returned_letters)

    @patch('builtins.input', side_effect=['aaaaaaaaaa', '-1'])
    def test_manually_enter_letters_too_long(self, mock_input):
        """
        Tests the user is not allowed to enter a string that is too long

        Args:
            mock_input (MagicMock): The mocked input

        Asserts:
            The correct error message is shown and None is returned
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            returned_letters = manually_enter_letters()

        self.assertIn(
            "Error: Invalid Input, must be 9 letters", fake_out.getvalue()
        )
        self.assertIsNone(returned_letters)

    @patch('builtins.input', side_effect=['aaaaa!aaa', '-1'])
    def test_manually_enter_letters_none_letter(self, mock_input):
        """
        Tests the user is not allowed to enter a string that contains a symbol

        Args:
            mock_input (MagicMock): The mocked input

        Asserts:
            The correct error message is shown and None is returned
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            returned_letters = manually_enter_letters()

        self.assertIn(
            "Error: Invalid Input, must be 9 letters", fake_out.getvalue()
        )
        self.assertIsNone(returned_letters)

    @patch('builtins.input', side_effect=['', '-1'])
    def test_manually_enter_letters_empty(self, mock_input):
        """
        Tests the user is not allowed to not enter anything

        Args:
            mock_input (MagicMock): The mocked input

        Asserts:
            The correct error message is shown and None is returned
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            returned_letters = manually_enter_letters()

        self.assertIn(
            "Error: Invalid Input, must be 9 letters", fake_out.getvalue()
        )
        self.assertIsNone(returned_letters)

    @patch('builtins.input', return_value="1")
    @patch('CLI.Main.manually_enter_letters', return_value='aaaaaaaaa')
    def test_play_game_letter_generation_manually_enter(
        self,
        mock_manually_enter_letters: MagicMock,
        mock_input: MagicMock
    ):
        """
        Tests the letter generation selection when manually enter letters is
        selected

        Args:
            mock_manually_enter_letters (MagicMock): the mock of the manually
                enter letters function
            mock_input (MagicMock): The mock of the input

        Asserts:
            The correct function is called and the letters are returned
        """
        with patch('sys.stdout', new=StringIO()):
            returned_letters = play_game_letter_generation()

        mock_manually_enter_letters.assert_called_once()
        self.assertEqual(returned_letters, 'aaaaaaaaa')

    @patch('builtins.input', return_value="2")
    @patch('CLI.Main.draw_letters', return_value='aaaaaaaaa')
    def test_play_game_letter_generation_draw_letters(
        self,
        mock_draw_letters: MagicMock,
        mock_input: MagicMock
    ):
        """
        Tests the letter generation selection when manually enter letters is
        selected

        Args:
            mock_manually_enter_letters (MagicMock): the mock of the
                draw_letters function
            mock_input (MagicMock): The mock of the input

        Asserts:
            The correct function is called and the letters are returned
        """
        with patch('sys.stdout', new=StringIO()):
            returned_letters = play_game_letter_generation()

        mock_draw_letters.assert_called_once()
        self.assertEqual(returned_letters, 'aaaaaaaaa')

    @patch('builtins.input', return_value="-1")
    @patch('CLI.Main.manually_enter_letters', return_value='aaaaaaaaa')
    @patch('CLI.Main.draw_letters', return_value='bbbbbbbbb')
    def test_play_game_letter_generation_exit(
        self,
        mock_draw_letters: MagicMock,
        mock_manually_enter_letters: MagicMock,
        mock_input: MagicMock
    ):
        """
        Tests the letter generation selection when the user decides to exit

        Args:
            mock_draw_letters (MagicMock): the mock of the
                draw_letters function
            mock_manually_enter_letters (MagicMock): the mock of the manually
                enter letters function
            mock_input (MagicMock): The mock of the input

        Asserts:
            No functions are called and None is returned
        """
        with patch('sys.stdout', new=StringIO()):
            returned_letters = play_game_letter_generation()

        mock_draw_letters.assert_not_called()
        mock_manually_enter_letters.assert_not_called()
        self.assertIsNone(returned_letters)

    @patch('builtins.input', side_effect=["3", "-1"])
    @patch('CLI.Main.manually_enter_letters', return_value='aaaaaaaaa')
    @patch('CLI.Main.draw_letters', return_value='bbbbbbbbb')
    def test_play_game_letter_generation_invalid_choice(
        self,
        mock_draw_letters: MagicMock,
        mock_manually_enter_letters: MagicMock,
        mock_input: MagicMock
    ):
        """
        Tests the letter generation selection when the user gives an invalid
        choice

        Args:
            mock_draw_letters (MagicMock): the mock of the
                draw_letters function
            mock_manually_enter_letters (MagicMock): the mock of the manually
                enter letters function
            mock_input (MagicMock): The mock of the input

        Asserts:
            No functions are called and None is returned
        """
        with patch('sys.stdout', new=StringIO()):
            returned_letters = play_game_letter_generation()

        mock_draw_letters.assert_not_called()
        mock_manually_enter_letters.assert_not_called()
        self.assertIsNone(returned_letters)

    @patch('CLI.Main.play_game_letter_generation', return_value=None)
    def test_command_play_game_no_letters(
        self,
        mock_play_game_letter_generation: MagicMock
    ):
        """
        Tests the play game function when no letters were generated

        Args:
            mock_play_game_letter_generation (MagicMock): The mock of the
                letter generation function simulating the user exitting
                without generating letters

        Asserts:
            The function returns without proceeding further
        """
        with patch('sys.stdout', new=StringIO()) as fake_out:
            command_play_game({})

        self.assertNotIn("input a word (or -1 to see answers): ", fake_out)

    @patch('CLI.Main.play_game_letter_generation', return_value="aaaaaaaaa")
    @patch('builtins.input', side_effect=["aaaa", '-1'])
    @patch('CLI.Main.check_answer')
    @patch('CLI.Main.solve_countdown')
    @patch('CLI.Main.output_words')
    def test_command_play_game_all_valid(
        self,
        mock_output_words: MagicMock,
        mock_solve_countdown: MagicMock,
        mock_check_answer: MagicMock,
        mock_input: MagicMock,
        mock_play_game_letter_generation: MagicMock
    ):
        """
        Tests the play game function when valid inputs are given

        Args:
            mock_output_words (MagicMock): The mock of the output words
                function to ensure the correct answers are given
            mock_solve_countdown (MagicMock): The mock of the solve countdown
                function to ensure the correct answers are retrieved
            mock_check_answer (MagicMock): The mock of the check answer
                function for if a valid word is sent and registered as correct
                with 2 definitions
            mock_input (MagicMock): The mock of the input for the user
                inputting a valid word then exitting
            mock_play_game_letter_generation (MagicMock): The mock of the
                letter generation function

        Asserts:
            The definitions are outputted correctly and the function returns
            when used correctly
        """
        mock_check_answer.return_value = {
            "correct": True,
            "definitions": [
                "3 as",
                "what is this"
            ]
        }
        with patch('sys.stdout', new=StringIO()) as fake_out:
            command_play_game({})

        mock_play_game_letter_generation.assert_called_once()
        mock_check_answer.assert_called_once()
        self.assertNotIn("Invalid Guess", fake_out.getvalue())
        self.assertNotIn("incorrect", fake_out.getvalue())
        self.assertIn("correct", fake_out.getvalue())
        self.assertIn("Word Definitions:", fake_out.getvalue())
        self.assertIn("3 as", fake_out.getvalue())
        self.assertIn("what is this", fake_out.getvalue())

        mock_solve_countdown.assert_called_once()
        mock_output_words.assert_called_once()

    @patch('CLI.Main.play_game_letter_generation', return_value="aaaaaaaaa")
    @patch('builtins.input', side_effect=["aaaa", '-1'])
    @patch('CLI.Main.check_answer')
    @patch('CLI.Main.solve_countdown')
    @patch('CLI.Main.output_words')
    def test_command_play_game_incorrect_guess(
        self,
        mock_output_words: MagicMock,
        mock_solve_countdown: MagicMock,
        mock_check_answer: MagicMock,
        mock_input: MagicMock,
        mock_play_game_letter_generation: MagicMock
    ):
        """
        Tests the play game function when a guess is incorrect

        Args:
            mock_output_words (MagicMock): The mock of the output words
                function to ensure the correct answers are given
            mock_solve_countdown (MagicMock): The mock of the solve countdown
                function to ensure the correct answers are retrieved
            mock_check_answer (MagicMock): The mock of the check answer
                function for if a valid word is sent and registered as
                incorrect
            mock_input (MagicMock): The mock of the input for the user
                inputting a valid word that's incorrect then exitting
            mock_play_game_letter_generation (MagicMock): The mock of the
                letter generation function

        Asserts:
            incorrect is outputted and the function returns properly
        """
        mock_check_answer.return_value = {
            "correct": False,
            "definitions": []
        }
        with patch('sys.stdout', new=StringIO()) as fake_out:
            command_play_game({})

        mock_play_game_letter_generation.assert_called_once()
        mock_check_answer.assert_called_once()
        self.assertNotIn("Invalid Guess", fake_out.getvalue())
        self.assertIn("incorrect", fake_out.getvalue())
        self.assertNotIn("Word Definitions:", fake_out.getvalue())

        mock_solve_countdown.assert_called_once()
        mock_output_words.assert_called_once()

    @patch('CLI.Main.play_game_letter_generation', return_value="aaaaaaaaa")
    @patch('builtins.input', side_effect=["aaaa", "bbbb", '-1'])
    @patch('CLI.Main.check_answer')
    @patch('CLI.Main.solve_countdown')
    @patch('CLI.Main.output_words')
    def test_command_play_game_multiple_answers(
        self,
        mock_output_words: MagicMock,
        mock_solve_countdown: MagicMock,
        mock_check_answer: MagicMock,
        mock_input: MagicMock,
        mock_play_game_letter_generation: MagicMock
    ):
        """
        Tests the play game function when multiple valid inputs are given

        Args:
            mock_output_words (MagicMock): The mock of the output words
                function to ensure the correct answers are given
            mock_solve_countdown (MagicMock): The mock of the solve countdown
                function to ensure the correct answers are retrieved
            mock_check_answer (MagicMock): The mock of the check answer
                function for if a valid word is sent and registered as correct
                with 2 definitions
            mock_input (MagicMock): The mock of the input for the user
                inputting 2 valid words then exitting
            mock_play_game_letter_generation (MagicMock): The mock of the
                letter generation function

        Asserts:
            Both answers and their definitions are outputted correctly and the
            function returns when used correctly
        """
        mock_check_answer.side_effect = [
            {
                "correct": True,
                "definitions": [
                    "3 as",
                    "what is this"
                ]
            },
            {
                "correct": True,
                "definitions": [
                    "2nd word definition",
                ]
            }
        ]
        with patch('sys.stdout', new=StringIO()) as fake_out:
            command_play_game({})

        mock_play_game_letter_generation.assert_called_once()
        mock_check_answer.assert_has_calls([
            call('aaaa', 'aaaaaaaaa', {}),
            call('bbbb', 'aaaaaaaaa', {})
        ])
        self.assertNotIn("Invalid Guess", fake_out.getvalue())
        self.assertNotIn("incorrect", fake_out.getvalue())
        self.assertIn("correct", fake_out.getvalue())
        self.assertIn("Word Definitions:", fake_out.getvalue())
        self.assertIn("3 as", fake_out.getvalue())
        self.assertIn("what is this", fake_out.getvalue())
        self.assertIn("2nd word definition", fake_out.getvalue())

        mock_solve_countdown.assert_called_once()
        mock_output_words.assert_called_once()

    @patch('CLI.Main.play_game_letter_generation', return_value="aaaaaaaaa")
    @patch('builtins.input', side_effect=["aaaaaaaaaa", '-1'])
    @patch('CLI.Main.check_answer')
    @patch('CLI.Main.solve_countdown')
    @patch('CLI.Main.output_words')
    def test_command_play_game_guess_too_long(
        self,
        mock_output_words: MagicMock,
        mock_solve_countdown: MagicMock,
        mock_check_answer: MagicMock,
        mock_input: MagicMock,
        mock_play_game_letter_generation: MagicMock
    ):
        """
        Tests the play game function when a word too long is given

        Args:
            mock_output_words (MagicMock): The mock of the output words
                function to ensure the correct answers are given
            mock_solve_countdown (MagicMock): The mock of the solve countdown
                function to ensure the correct answers are retrieved
            mock_check_answer (MagicMock): The mock of the check answer
                function for if a valid word is sent and registered as correct
                with 2 definitions
            mock_input (MagicMock): The mock of the input for the user
                inputting an invalid word then exitting
            mock_play_game_letter_generation (MagicMock): The mock of the
                letter generation function

        Asserts:
            The appropriate message is given
        """
        mock_check_answer.return_value = {
            "correct": True,
            "definitions": [
                "3 as",
                "what is this"
            ]
        }
        with patch('sys.stdout', new=StringIO()) as fake_out:
            command_play_game({})

        mock_play_game_letter_generation.assert_called_once()
        mock_check_answer.assert_not_called()
        self.assertNotIn("incorrect", fake_out.getvalue())
        self.assertNotIn("correct", fake_out.getvalue())
        self.assertIn("Invalid Guess", fake_out.getvalue())

        mock_solve_countdown.assert_called_once()
        mock_output_words.assert_called_once()

    @patch('CLI.Main.play_game_letter_generation', return_value="aaaaaaaaa")
    @patch('builtins.input', side_effect=["aaa!", '-1'])
    @patch('CLI.Main.check_answer')
    @patch('CLI.Main.solve_countdown')
    @patch('CLI.Main.output_words')
    def test_command_play_game_non_alpha(
        self,
        mock_output_words: MagicMock,
        mock_solve_countdown: MagicMock,
        mock_check_answer: MagicMock,
        mock_input: MagicMock,
        mock_play_game_letter_generation: MagicMock
    ):
        """
        Tests the play game function when a word containing a non letter is
        inputted

        Args:
            mock_output_words (MagicMock): The mock of the output words
                function to ensure the correct answers are given
            mock_solve_countdown (MagicMock): The mock of the solve countdown
                function to ensure the correct answers are retrieved
            mock_check_answer (MagicMock): The mock of the check answer
                function for if a valid word is sent and registered as correct
                with 2 definitions
            mock_input (MagicMock): The mock of the input for the user
                inputting an invalid word then exitting
            mock_play_game_letter_generation (MagicMock): The mock of the
                letter generation function

        Asserts:
            The appropriate message is given
        """
        mock_check_answer.return_value = {
            "correct": True,
            "definitions": [
                "3 as",
                "what is this"
            ]
        }
        with patch('sys.stdout', new=StringIO()) as fake_out:
            command_play_game({})

        mock_play_game_letter_generation.assert_called_once()
        mock_check_answer.assert_not_called()
        self.assertNotIn("incorrect", fake_out.getvalue())
        self.assertNotIn("correct", fake_out.getvalue())
        self.assertIn("Invalid Guess", fake_out.getvalue())

        mock_solve_countdown.assert_called_once()
        mock_output_words.assert_called_once()


if __name__ == '__main__':
    unittest.main()
