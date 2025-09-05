# Hangman Word Guessing Game Development Report

## 1. Introduction

### 1.1 Project Objectives
This project aims to develop a complete Hangman word guessing game program with the following core functionalities:
- Two game levels: Basic mode (words) and Intermediate mode (phrases).
- 15-second countdown mechanism.
- Life system (6 lives).
- Graphical user interface.
- Comprehensive input validation and error handling.

### 1.2 Technology Selection Rationale

**Programming Language: Python**

- **Simple and Readable**: Python's clear syntax makes it suitable for rapid development and maintenance.
- **Rich GUI Libraries**: Built-in tkinter library requires no additional installation.
- **Cross-platform Compatibility**: Supports Windows, macOS, and Linux.
- **Strong Testing Support**: Excellent testing frameworks like pytest.

**Automated Unit Testing Tool: pytest**
- **Simple and Easy to Use**: Concise syntax with a low learning curve.
- **Powerful Features**: Supports parameterized tests, fixtures, mocks, and other advanced features.
- **Rich Plugin Ecosystem**: Plugins like pytest-cov for code coverage analysis.
- **Detailed Reports**: Provides precise test results and failure information.

## 2. Process

### 2.1 Project Initialisation and Environment Setup

First, create a project structure and install necessary dependencies:

```bash
# Testing dependencies
pytest>=8.0.0
pytest-cov>=4.0.0

# Code quality tools
pylint>=3.0.0
```

### 2.2 Test-Driven Development (TDD) Implementation

#### 2.2.1 Creating Word and Phrase Dictionary
**Requirement**: Provide valid English words and phrases as game content.

**TDD Process**:
1. First, create a `words.py` file, defining basic words and intermediate phrase lists.
2. Include 50 basic words and 50 intermediate phrases.
3. All vocabulary is valid English words/phrases.

```python
"""
Hangman Game Word and Phrase Dictionary
Contains vocabulary for basic mode (words) and intermediate mode (phrases)
"""

# Basic Mode - Single Words
BASIC_WORDS = [
    "python", "computer", "programming", "algorithm", "function",
    "variable", "string", "integer", "boolean", "dictionary",
    "list", "tuple", "loop", "condition", "class", "object",
    "method", "inheritance", "polymorphism", "encapsulation",
    "abstraction", "recursion", "iteration", "debugging", "testing",
    "framework", "library", "module", "package", "import",
    "exception", "error", "syntax", "semantic", "compiler",
    "interpreter", "runtime", "memory", "stack", "queue",
    "tree", "graph", "hash", "sort", "search", "binary",
    "linear", "recursive", "iterative", "optimization",
    "hello", "world", "game", "player", "guess", "letter",
    "word", "phrase", "level", "difficulty", "challenge",
    "victory", "defeat", "success", "failure", "attempt"
]

# Intermediate Mode - Phrases
INTERMEDIATE_PHRASES = [
    "artificial intelligence",
    "machine learning",
    "data science",
    "web development",
    "mobile application",
    "user interface",
    "user experience",
    "database management",
    "software engineering",
    "version control",
    "agile methodology",
    "test driven development",
    "object oriented programming",
    "functional programming",
    "cloud computing",
    "cyber security",
    "network administration",
    "system architecture",
    "application programming interface",
    "representational state transfer",
    "structured query language",
    "hypertext markup language",
    "cascading style sheets",
    "javascript object notation",
    "extensible markup language",
    "simple object access protocol",
    "domain name system",
    "transmission control protocol",
    "internet protocol",
    "file transfer protocol",
    "hypertext transfer protocol",
    "secure sockets layer",
    "transport layer security",
    "public key infrastructure",
    "virtual private network",
    "local area network",
    "wide area network",
    "wireless fidelity",
    "bluetooth technology",
    "near field communication",
    "hello world",
    "good morning",
    "thank you",
    "you are welcome",
    "have a nice day",
    "see you later",
    "take care",
    "best wishes",
    "happy birthday",
    "merry christmas"
]

```

#### 2.2.2 Game Core Logic Development
**Requirement**: Implement game rules, guess processing, and win/lose determination.

1. Write test cases first (`test_hangman.py`).
2. Implement the `HangmanGame` class to pass the test. 
3. Refactor code while maintaining test coverage.

**Key Test Cases**:
```python
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

    def test_correct_letter_guess(self):
        """Test correct letter guess"""
        with patch('hangman_game.random.choice', return_value='python'):
            game = HangmanGame(GameLevel.BASIC)
            result = game.make_guess('p')
            assert result['success'] is True
            assert result['message'] == 'Correct guess!'
            assert 'p' in game.display_word
            assert game.lives == game.max_lives  # Lives should not decrease
```

**Implementation Results**:

- Created `HangmanGame` class with complete game logic.
- Implemented `GameLevel` enum to define game levels.
- Supports both word and phrase modes.
- Comprehensive input validation and error handling.

#### 2.2.3 Graphical User Interface Development
**Requirement**: Create a modern GUI interface.

**TDD Process**:
1. First, create `the HangmanGUI` class.
2. Implement a clean interface design.
3. Integrate game logic.

**Interface Features**:
- Clear visual hierarchy.
- Real-time game state display.
- User-friendly input validation.
- Keyboard support (Enter key confirmation).

#### 2.2.4 Test Coverage and Verification

**Test Statistics**:
- Total test cases: 22.
- Test pass rate: 100%.
- Coverage scope: Game logic, integration tests, edge cases.

**Test Run Results**:

<img src="E:\Python\Hangman\screenshots\Unit Test.png" style="zoom:75%;" />

### 2.3 Functional Requirements Implementation Verification

#### 2.3.1 Game Level Implementation
- **Basic Mode**: Random word generation.
- **Intermediate Mode**: Random phrase generation.
- Implemented level selection interface.

#### 2.3.2 Dictionary Validation
- Created basic dictionary with 50 words.
- Created an intermediate dictionary with 50 phrases.
- All vocabulary is valid English words/phrases.

#### 2.3.3 Underscore Display
- Word display: `_ _ _ _ _ _`
- Phrase display: `_ _ _ _ _   _ _ _ _ _`
- Correct guesses reveal letters.

#### 2.3.4 Life System
- Initial six lives.
- Wrong guesses deduct one life.
- Real-time life display.

#### 2.3.5 Win/Lose Conditions
- Win: Guess all letters.
- Lose: Lives exhausted.
- Display the correct answer when the game ends.

#### 2.3.6 Game Loop
- Support continuous gameplay.
- Ask to play again after the game ends.
- Can exit the game anytime.

### 2.4. Project Optimisation and Cleanup

- Checked using pylint, and all warnings were fixed.

  <img src="E:\Python\Hangman\screenshots\Static Analysis.png" style="zoom:75%;" />

- Simplified GUI interface, focusing on core functionality.

- Cleaned up debug and useless files.

### 2.5. Screenshots of runtime

#### 2.5.1 Game Level Selection
<img src="E:\Python\Hangman\screenshots\Game Level.png" alt="Game Level" style="zoom:50%;" />

#### 2.5.2 Guessing with Countdown Timer
<img src="E:\Python\Hangman\screenshots\Guessing.png" alt="Guessing" style="zoom:50%;" />

#### 2.5.3 Game Failed

<img src="E:\Python\Hangman\screenshots\Game Failed.png" alt="Game Failed" style="zoom:50%;" />

#### 2.5.4 Game Won

<img src="E:\Python\Hangman\screenshots\Game Won.png" alt="Game Won" style="zoom:50%;" />

## 3 Conclusion
  Repository: https://github.com/Jeremy0730/Hangman

### 3.1 Key Achievements

1. **Test-Driven Development (TDD) Practice**
   - Ensured code quality and functional correctness through a test-first approach.
   - 22 test cases with 100% pass rate, proving the effectiveness of the TDD method effectiveness.
   - Test cases not only verify functionality but also serve as code documentation.

2. **Python GUI Programming Experience**
   - Mastered basic usage of the tkinter library.
   - Learned to create responsive user interfaces.
   - Understood event-driven programming patterns for GUI applications.

3. **Software Engineering Best Practices**
   - Modular design: Clear separation of responsibilities.
   - Error handling: Comprehensive exception handling mechanisms.
   - Code standards: Consistent code style and documentation comments.

### 3.2 Technical Experience

1. **Advantages of the Pytest Testing Framework**
   - Concise syntax, easy to write and maintain test cases.
   - Supports mocks and patches, facilitating unit testing.
   - Provides detailed test reports and failure information.

2. **TDD Development Process Insights**
   - Red-Green-Refactor cycle ensures code quality.
   - Test cases serve as requirement documentation, clarifying functional specifications.
   - The refactoring process is safer with test protection.

3. **Project Management and Code Organisation**
   - A clear project structure facilitates maintenance.
   - Appropriate documentation and comments improve code readability.
   - Importance of version control and dependency management.

### 3.3 Project Results

- **Complete Functionality**: Implemented all required functional requirements.
- **High Code Quality**: Ensured code correctness through TDD.
- **User-Friendly**: Simple and intuitive graphical interface.
- **Maintainable**: Clear code structure and comprehensive test coverage.
