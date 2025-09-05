# 🎯 Hangman Word Guessing Game

A classic Hangman word guessing game with a graphical user interface, developed using Python and tkinter.

## ✨ Features

- **🎮 Two Game Levels**:
  - Basic Mode: Random word generation
  - Intermediate Mode: Random phrase generation
- **❤️ Life System**: 6 lives, deducted for wrong guesses
- **🎨 Clean Interface**: Clear and user-friendly graphical interface
- **📝 Input Validation**: Comprehensive input validation and error handling

## 🚀 Quick Start

### Requirements
- Python 3.6 or higher
- tkinter (usually comes with Python)

### Run the Game

```bash
python main.py
```

Or run the GUI version directly:
```bash
python minimal_gui.py
```

## 🎮 Game Rules

1. **Select Level**: Choose Basic Mode (words) or Intermediate Mode (phrases)
2. **Start Guessing**: Enter a letter in the input box
3. **Lives**: Start with 6 lives
4. **Win Condition**: Guess all letters before lives are exhausted
5. **Lose Condition**: Lives are exhausted

## 📁 Project Structure

```
hangman-game/
├── minimal_gui.py       # Graphical user interface
├── hangman_game.py      # Game core logic
├── words.py             # Word and phrase dictionary
├── test_hangman.py      # Game logic tests
├── requirements.txt     # Dependencies
├── .gitignore          # Git ignore file
├── README.md           # Project documentation
└── Project Report.md   # Project report
```

## 🧪 Running Tests

Install test dependencies:
```bash
pip install -r requirements.txt
```

Run tests:
```bash
python -m pytest test_hangman.py -v
```

## 🔧 Technical Implementation

### Core Components

1. **HangmanGame Class**: Game core logic
   - Word/phrase selection
   - Guess processing
   - Win/lose determination

2. **MinimalHangmanGUI Class**: Graphical user interface
   - Game state display
   - User input handling
   - Clean interface design

3. **GameLevel Enum**: Game levels
   - BASIC: Basic mode
   - INTERMEDIATE: Intermediate mode

### Key Features

- **Input Validation**: Comprehensive input validation and error handling
- **Clean Interface**: Clear and user-friendly GUI design
- **Test Coverage**: Comprehensive unit tests

## 📝 Development Notes

### Test-Driven Development (TDD)
The project uses test-driven development approach:
1. Write test cases first
2. Implement functionality to pass tests
3. Refactor code while maintaining test coverage

### Code Structure
- Clear module separation
- Comprehensive error handling
- Detailed documentation comments
- Consistent code style

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Developed to demonstrate Python GUI programming and test-driven development.

---

**Enjoy the game! 🎮**
