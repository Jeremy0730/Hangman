"""
Hangman Game Core Logic
Implements game rules, timer, life management and other functions
"""

import random
import time
from enum import Enum
from words import BASIC_WORDS, INTERMEDIATE_PHRASES


class GameLevel(Enum):
    """Game difficulty level enumeration"""
    BASIC = "Basic Mode"
    INTERMEDIATE = "Intermediate Mode"


class HangmanGame:
    """Hangman Game Main Class"""

    def __init__(self, level: GameLevel):
        """
        Initialize game

        Args:
            level: Game difficulty level (basic or intermediate)
        """
        self.level = level
        self.max_lives = 6
        self.lives = self.max_lives
        self.guessed_letters = set()

        # Timer configuration
        self.timer_start = None
        self.timer_duration = 15  # 15 second timer

        # Game content (word/phrase and their displays)
        self.game_content = {}
        if level == GameLevel.BASIC:
            self.game_content = {
                'word': random.choice(BASIC_WORDS).lower(),
                'phrase': None,
                'display_word': None,
                'display_phrase': None
            }
            self.game_content['display_word'] = self._create_display_word()
        else:
            self.game_content = {
                'word': None,
                'phrase': random.choice(INTERMEDIATE_PHRASES).lower(),
                'display_word': None,
                'display_phrase': None
            }
            self.game_content['display_phrase'] = self._create_display_phrase()

    def _create_display_word(self) -> str:
        """Create display string for word (using underscores for unguessed letters)"""
        return ' '.join('_' for _ in self.game_content['word'])

    def _create_display_phrase(self) -> str:
        """Create display string for phrase (using underscores for unguessed letters)"""
        result = []
        for char in self.game_content['phrase']:
            if char == ' ':
                result.append(' ')
            else:
                result.append('_')
        return ' '.join(result)

    def start_timer(self):
        """Start timer"""
        self.timer_start = time.time()

    def check_timer(self) -> bool:
        """
        Check if timer has expired, deduct life if timeout

        Returns:
            True if timer expired, False otherwise
        """
        if self.timer_start is None:
            return False

        elapsed = time.time() - self.timer_start
        if elapsed >= self.timer_duration:
            self.lives -= 1
            self.timer_start = None
            return True
        return False

    def get_remaining_time(self) -> int:
        """
        Get remaining time

        Returns:
            Remaining seconds, returns 0 if timer not started
        """
        if self.timer_start is None:
            return 0

        elapsed = time.time() - self.timer_start
        remaining = max(0, self.timer_duration - int(elapsed))
        return remaining

    def make_guess(self, letter: str) -> dict:
        """
        Make letter guess

        Args:
            letter: Letter to guess

        Returns:
            Dictionary containing success status and message
        """
        # Validate input
        letter = letter.strip()
        if not letter or len(letter) != 1:
            return {
                'success': False,
                'message': 'Please enter a single letter.'
            }

        letter = letter.lower()

        if not letter.isalpha():
            return {
                'success': False,
                'message': 'Please enter a valid letter.'
            }

        if letter in self.guessed_letters:
            return {
                'success': False,
                'message': f'You have already guessed the letter "{letter}".'
            }

        # Add to guessed letters set
        self.guessed_letters.add(letter)

        # Check if letter is in word/phrase
        if self.level == GameLevel.BASIC:
            if letter in self.game_content['word']:
                self._update_display_word(letter)
                return {
                    'success': True,
                    'message': 'Correct guess!'
                }
        else:
            if letter in self.game_content['phrase']:
                self._update_display_phrase(letter)
                return {
                    'success': True,
                    'message': 'Correct guess!'
                }

        # Wrong guess - deduct life
        self.lives -= 1
        return {
            'success': False,
            'message': 'Wrong guess! You lost a life.'
        }

    def _update_display_word(self, letter: str):
        """Update word display, show correctly guessed letters"""
        display_chars = list(self.game_content['display_word'].replace(' ', ''))
        for i, char in enumerate(self.game_content['word']):
            if char == letter:
                display_chars[i] = letter
        self.game_content['display_word'] = ' '.join(display_chars)

    def _update_display_phrase(self, letter: str):
        """Update phrase display, show correctly guessed letters"""
        # Convert display phrase to list, preserve spaces
        display_list = list(self.game_content['display_phrase'])
        phrase_list = list(self.game_content['phrase'])

        for i, char in enumerate(phrase_list):
            if (char == letter and
                display_list[i * 2] == '_'):
                display_list[i * 2] = letter

        self.game_content['display_phrase'] = ''.join(display_list)

    def is_game_won(self) -> bool:
        """
        Check if game is won

        Returns:
            True if all letters have been guessed, False otherwise
        """
        if self.level == GameLevel.BASIC:
            return '_' not in self.game_content['display_word']
        return '_' not in self.game_content['display_phrase']

    def is_game_lost(self) -> bool:
        """
        Check if game is lost

        Returns:
            True if lives are exhausted, False otherwise
        """
        return self.lives <= 0

    def get_current_display(self) -> str:
        """
        Get current display string

        Returns:
            Current display string, guessed letters will be shown
        """
        if self.level == GameLevel.BASIC:
            return self.game_content['display_word']
        return self.game_content['display_phrase']

    def get_answer(self) -> str:
        """
        Get answer (word or phrase)

        Returns:
            Complete answer
        """
        if self.level == GameLevel.BASIC:
            return self.game_content['word']
        return self.game_content['phrase']

    def get_wrong_guesses_count(self) -> int:
        """
        Get number of wrong guesses

        Returns:
            Number of wrong guesses
        """
        return self.max_lives - self.lives

    # Backward compatibility properties
    @property
    def word(self):
        """Get current word (for backward compatibility)"""
        return self.game_content.get('word')

    @property
    def phrase(self):
        """Get current phrase (for backward compatibility)"""
        return self.game_content.get('phrase')

    @property
    def display_word(self):
        """Get current word display (for backward compatibility)"""
        return self.game_content.get('display_word')

    @property
    def display_phrase(self):
        """Get current phrase display (for backward compatibility)"""
        return self.game_content.get('display_phrase')
