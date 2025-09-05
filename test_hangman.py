"""
Hangman Game Unit Tests
Test-driven development using pytest
"""

import time
from unittest.mock import patch

from hangman_game import HangmanGame, GameLevel
from words import BASIC_WORDS, INTERMEDIATE_PHRASES


class TestHangmanGame:
    """Test cases for HangmanGame class"""

    def test_game_initialization_basic_level(self):
        """Test basic level game initialization"""
        game = HangmanGame(GameLevel.BASIC)
        assert game.level == GameLevel.BASIC
        assert game.lives == 6
        assert game.max_lives == 6
        assert game.word is not None
        assert len(game.word) > 0
        assert game.guessed_letters == set()
        assert game.display_word.count('_') > 0

    def test_game_initialization_intermediate_level(self):
        """Test intermediate level game initialization"""
        game = HangmanGame(GameLevel.INTERMEDIATE)
        assert game.level == GameLevel.INTERMEDIATE
        assert game.lives == 6
        assert game.max_lives == 6
        assert game.phrase is not None
        assert len(game.phrase) > 0
        assert game.guessed_letters == set()
        assert game.display_phrase.count('_') > 0

    def test_display_word_format(self):
        """Test word display format"""
        with patch('hangman_game.random.choice', return_value='python'):
            game = HangmanGame(GameLevel.BASIC)
            assert game.display_word == '_ _ _ _ _ _'

    def test_display_phrase_format(self):
        """Test phrase display format"""
        with patch('hangman_game.random.choice', return_value='hello world'):
            game = HangmanGame(GameLevel.INTERMEDIATE)
            assert game.display_phrase == '_ _ _ _ _   _ _ _ _ _'

    def test_correct_letter_guess(self):
        """Test correct letter guess"""
        with patch('hangman_game.random.choice', return_value='python'):
            game = HangmanGame(GameLevel.BASIC)
            result = game.make_guess('p')
            assert result['success'] is True
            assert result['message'] == 'Correct guess!'
            assert 'p' in game.display_word
            assert game.lives == game.max_lives  # Lives should not decrease

    def test_incorrect_letter_guess(self):
        """Test incorrect letter guess"""
        with patch('hangman_game.random.choice', return_value='python'):
            game = HangmanGame(GameLevel.BASIC)
            initial_lives = game.lives
            result = game.make_guess('z')
            assert result['success'] is False
            assert result['message'] == 'Wrong guess! You lost a life.'
            assert game.lives == initial_lives - 1

    def test_duplicate_letter_guess(self):
        """Test duplicate letter guess"""
        with patch('hangman_game.random.choice', return_value='python'):
            game = HangmanGame(GameLevel.BASIC)
            game.make_guess('p')
            result = game.make_guess('p')
            assert result['success'] is False
            assert 'already guessed' in result['message']

    def test_game_won_condition(self):
        """Test game won condition"""
        with patch('hangman_game.random.choice', return_value='hi'):
            game = HangmanGame(GameLevel.BASIC)
            game.make_guess('h')
            game.make_guess('i')
            assert game.is_game_won() is True

    def test_game_lost_condition(self):
        """Test game lost condition"""
        with patch('hangman_game.random.choice', return_value='python'):
            game = HangmanGame(GameLevel.BASIC)
            game.lives = 1
            game.make_guess('z')
            assert game.is_game_lost() is True

    def test_timer_functionality(self):
        """Test timer functionality"""
        with patch('hangman_game.random.choice', return_value='python'):
            game = HangmanGame(GameLevel.BASIC)
            initial_lives = game.lives

            # Simulate timeout
            with patch('time.time', side_effect=[0, 16]):  # 16 seconds passed
                game.start_timer()
                time.sleep(0.1)  # Small delay to ensure timer check
                game.check_timer()

            assert game.lives == initial_lives - 1

    def test_phrase_guessing(self):
        """Test phrase guessing"""
        with patch('hangman_game.random.choice', return_value='hello world'):
            game = HangmanGame(GameLevel.INTERMEDIATE)
            result = game.make_guess('l')
            assert result['success'] is True
            # 'l' appears 3 times in 'hello world'
            assert game.display_phrase.count('l') == 3

    def test_invalid_input_handling(self):
        """Test invalid input handling"""
        with patch('hangman_game.random.choice', return_value='python'):
            game = HangmanGame(GameLevel.BASIC)

            # Test empty input
            result = game.make_guess('')
            assert result['success'] is False
            assert 'single letter' in result['message']

            # Test multiple characters
            result = game.make_guess('ab')
            assert result['success'] is False
            assert 'single letter' in result['message']

            # Test non-alphabetic character
            result = game.make_guess('1')
            assert result['success'] is False
            assert 'valid letter' in result['message']

    def test_get_remaining_time(self):
        """Test get remaining time"""
        with patch('hangman_game.random.choice', return_value='python'):
            game = HangmanGame(GameLevel.BASIC)

            # When timer not started
            assert game.get_remaining_time() == 0

            # When timer started
            with patch('time.time', return_value=0):
                game.start_timer()
                assert game.get_remaining_time() == 15

    def test_get_wrong_guesses_count(self):
        """Test get wrong guesses count"""
        with patch('hangman_game.random.choice', return_value='python'):
            game = HangmanGame(GameLevel.BASIC)

            # Initial state
            assert game.get_wrong_guesses_count() == 0

            # After wrong guess
            game.make_guess('z')
            assert game.get_wrong_guesses_count() == 1

            game.make_guess('x')
            assert game.get_wrong_guesses_count() == 2


class TestGameLevel:
    """Test cases for GameLevel enum"""

    def test_game_level_values(self):
        """Test game level values"""
        assert GameLevel.BASIC.value == "Basic Mode"
        assert GameLevel.INTERMEDIATE.value == "Intermediate Mode"

    def test_game_level_enumeration(self):
        """Test game level enumeration properties"""
        # Test that both levels exist
        levels = list(GameLevel)
        assert len(levels) == 2
        assert GameLevel.BASIC in levels
        assert GameLevel.INTERMEDIATE in levels

        # Test that values are strings
        for level in levels:
            assert isinstance(level.value, str)
            assert len(level.value) > 0


class TestGameIntegration:
    """Game integration tests"""

    def test_complete_basic_game_flow(self):
        """Test complete basic mode game flow"""
        with patch('hangman_game.random.choice', return_value='hi'):
            game = HangmanGame(GameLevel.BASIC)

            # Make correct guesses
            result1 = game.make_guess('h')
            assert result1['success'] is True

            result2 = game.make_guess('i')
            assert result2['success'] is True

            # Game should be won
            assert game.is_game_won() is True
            assert game.is_game_lost() is False

    def test_complete_intermediate_game_flow(self):
        """Test complete intermediate mode game flow"""
        with patch('hangman_game.random.choice', return_value='hi there'):
            game = HangmanGame(GameLevel.INTERMEDIATE)

            # Make correct guesses
            letters = ['h', 'i', 't', 'e', 'r']
            for letter in letters:
                result = game.make_guess(letter)
                assert result['success'] is True

            # Game should be won
            assert game.is_game_won() is True
            assert game.is_game_lost() is False

    def test_game_lost_flow(self):
        """Test game lost flow"""
        with patch('hangman_game.random.choice', return_value='test'):
            game = HangmanGame(GameLevel.BASIC)

            # Make wrong guesses to lose all lives
            wrong_letters = ['z', 'x', 'q', 'w', 'r', 'y']
            for letter in wrong_letters:
                result = game.make_guess(letter)
                assert result['success'] is False

            # Game should be lost
            assert game.is_game_lost() is True
            assert game.is_game_won() is False


class TestEdgeCases:
    """Edge case tests"""

    def test_empty_word_handling(self):
        """Test empty word handling"""

        # Ensure no empty strings in word lists
        for word in BASIC_WORDS:
            assert len(word.strip()) > 0, f"Found empty word: '{word}'"
            assert word.isalpha() or ' ' in word, f"Found invalid word: '{word}'"

        for phrase in INTERMEDIATE_PHRASES:
            assert len(phrase.strip()) > 0, f"Found empty phrase: '{phrase}'"
            assert phrase.replace(' ', '').isalpha(), f"Found invalid phrase: '{phrase}'"

    def test_special_characters_in_input(self):
        """Test special characters in input handling"""
        with patch('hangman_game.random.choice', return_value='test'):
            game = HangmanGame(GameLevel.BASIC)

            # Test various invalid inputs
            invalid_inputs = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')',
                            '-', '+', '=', '[', ']', '{', '}', '|', '\\', ';',
                            ':', '"', "'", '<', '>', ',', '.', '?', '/', '`', '~']

            for invalid_input in invalid_inputs:
                result = game.make_guess(invalid_input)
                assert result['success'] is False
                assert 'valid letter' in result['message']

    def test_case_insensitive_guessing(self):
        """Test case insensitive guessing"""
        with patch('hangman_game.random.choice', return_value='Test'):
            game = HangmanGame(GameLevel.BASIC)

            # Test uppercase guess
            result1 = game.make_guess('T')
            assert result1['success'] is True

            # Test lowercase guess for same letter
            result2 = game.make_guess('e')
            assert result2['success'] is True

    def test_whitespace_handling(self):
        """Test whitespace handling"""
        with patch('hangman_game.random.choice', return_value='test'):
            game = HangmanGame(GameLevel.BASIC)

            # Test input with leading/trailing spaces (should be stripped)
            result = game.make_guess('  t  ')
            assert result['success'] is True
