"""
Hangman Game GUI Module

This module provides a graphical user interface for the Hangman game
using tkinter. It includes timer functionality, game state management,
and user interaction handling.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import sys
from hangman_game import HangmanGame, GameLevel

class HangmanGUI:
    """Hangman GUI"""

    def __init__(self):
        """Initialize GUI"""
        self.root = tk.Tk()
        self.root.title("Hangman Game")
        self.root.geometry("600x400")

        # Game variables
        self.game = None
        self.timer_running = False
        self.timer_thread = None

        # GUI components grouped by category
        self.widgets = {}
        self.variables = {}

        self.create_widgets()
        self.show_main_menu()

    def create_widgets(self):
        """Create all GUI components"""
        # Main container
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Title
        self.title_label = ttk.Label(self.main_frame, text="Hangman Game")
        self.title_label.pack(pady=20)

        # Game info
        self.info_label = ttk.Label(self.main_frame, text="Lives: 6/6")
        self.info_label.pack(pady=10)

        # Timer display
        self.timer_label = ttk.Label(
            self.main_frame, text="Time: 15s",
            font=('Arial', 14, 'bold'), foreground='red')
        self.timer_label.pack(pady=5)

        # Word display
        self.word_label = ttk.Label(self.main_frame, text="", font=('Arial', 16))
        self.word_label.pack(pady=20)

        # Input frame
        self.input_frame = ttk.Frame(self.main_frame)
        self.input_frame.pack(pady=20)

        # Letter input
        self.letter_var = tk.StringVar()
        self.letter_entry = ttk.Entry(self.input_frame,
                                    textvariable=self.letter_var,
                                    width=5,
                                    justify='center')
        self.letter_entry.pack(side='left', padx=10)

        # Guess button
        self.guess_button = ttk.Button(self.input_frame,
                                     text="Guess",
                                     command=self.make_guess)
        self.guess_button.pack(side='left', padx=10)

        # Bind Enter key
        self.letter_entry.bind('<Return>', lambda e: self.make_guess())

        # Guessed letters display
        self.guessed_label = ttk.Label(self.main_frame, text="Guessed letters: None")
        self.guessed_label.pack(pady=10)

        # Level selection frame
        self.level_frame = ttk.Frame(self.main_frame)

        self.level_label = ttk.Label(self.level_frame, text="Select game level:")
        self.level_label.pack(pady=10)

        self.basic_button = ttk.Button(self.level_frame,
                                     text="Basic Mode (Words)",
                                     command=lambda: self.start_game(GameLevel.BASIC))
        self.basic_button.pack(pady=5)

        self.intermediate_button = ttk.Button(self.level_frame,
                                            text="Intermediate Mode (Phrases)",
                                            command=lambda: self.start_game(GameLevel.INTERMEDIATE))
        self.intermediate_button.pack(pady=5)

    def show_main_menu(self):
        """Show main menu"""
        self.hide_game_elements()
        self.level_frame.pack(pady=20)

    def hide_game_elements(self):
        """Hide game elements"""
        self.info_label.pack_forget()
        self.timer_label.pack_forget()
        self.word_label.pack_forget()
        self.input_frame.pack_forget()
        self.guessed_label.pack_forget()
        self.level_frame.pack_forget()

    def show_game_elements(self):
        """Show game elements"""
        self.level_frame.pack_forget()
        self.info_label.pack(pady=10)
        self.timer_label.pack(pady=5)
        self.word_label.pack(pady=20)
        self.input_frame.pack(pady=20)
        self.guessed_label.pack(pady=10)

    def start_game(self, level):
        """Start new game"""
        print(f"Starting game, level: {level}")
        self.game = HangmanGame(level)
        self.show_game_elements()
        self.update_display()

        # Ensure input box can receive input
        self.letter_entry.focus_set()
        self.letter_var.set("")

        print(f"Game started, input box state: {self.letter_entry['state']}")
        print(f"Input box has focus: {self.letter_entry.focus_get() == self.letter_entry}")

        # Start the timer for the first guess
        self.start_timer()

    def start_timer(self):
        """Start the 15-second timer"""
        if not self.game:
            return

        self.game.start_timer()
        self.timer_running = True

        # Start timer thread
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_running = False
            self.timer_thread.join()

        self.timer_thread = threading.Thread(target=self.timer_loop, daemon=True)
        self.timer_thread.start()

    def stop_timer(self):
        """Stop the timer"""
        self.timer_running = False
        if self.timer_thread and self.timer_thread.is_alive():
            self.timer_thread.join()

    def timer_loop(self):
        """Timer loop that runs in a separate thread"""
        while self.timer_running and self.game:
            remaining_time = self.game.get_remaining_time()

            # Update timer display in main thread
            self.root.after(0, self.update_timer_display, remaining_time)

            if remaining_time <= 0:
                # Time's up!
                self.root.after(0, self.handle_timeout)
                break

            time.sleep(1)  # Update every second

    def update_timer_display(self, remaining_time):
        """Update timer display (called from main thread)"""
        if remaining_time > 0:
            self.timer_label.config(text=f"Time: {remaining_time}s")
            # Change color based on remaining time
            if remaining_time <= 5:
                self.timer_label.config(foreground='red')
            elif remaining_time <= 10:
                self.timer_label.config(foreground='orange')
            else:
                self.timer_label.config(foreground='green')
        else:
            self.timer_label.config(text="Time: 0s", foreground='red')

    def handle_timeout(self):
        """Handle timer timeout"""
        if not self.game:
            return

        self.timer_running = False

        # Deduct life due to timeout
        self.game.lives -= 1
        self.timer_label.config(
            text="Time's up! Life lost!", foreground='red')

        # Show timeout message
        messagebox.showwarning(
            "Time's Up!",
            "Time's up! You lost a life. Try to guess faster next time!")

        # Update display
        self.update_display()

        # Check game status
        if self.game.is_game_lost():
            self.game_over("Game Over! Lives exhausted!")
        else:
            # Start timer for next guess
            self.start_timer()
            self.letter_entry.focus_set()

    def make_guess(self):
        """Handle letter guess"""
        print("make_guess called")
        if not self.game:
            print("Game not started")
            return

        letter = self.letter_var.get().strip().lower()
        print(f"Input letter: '{letter}'")

        if not letter:
            messagebox.showwarning("Invalid Input", "Please enter a letter!")
            return

        if len(letter) != 1 or not letter.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter!")
            self.letter_var.set("")
            return

        # Stop current timer
        self.stop_timer()

        result = self.game.make_guess(letter)
        self.letter_var.set("")

        print(f"Guess result: {result}")

        if result['success']:
            messagebox.showinfo("Correct!", result['message'])
        else:
            messagebox.showwarning("Wrong!", result['message'])

        self.update_display()

        # Check game status
        if self.game.is_game_won():
            self.stop_timer()
            self.game_over("Congratulations! You won!")
        elif self.game.is_game_lost():
            self.stop_timer()
            self.game_over("Game Over! Lives exhausted!")
        else:
            # Start timer for next guess
            self.start_timer()
            self.letter_entry.focus_set()

    def update_display(self):
        """Update game display"""
        if not self.game:
            return

        # Update lives
        self.info_label.config(text=f"Lives: {self.game.lives}/{self.game.max_lives}")

        # Update word display
        display_text = self.game.get_current_display()
        self.word_label.config(text=display_text)

        # Update guessed letters
        guessed_text = (', '.join(sorted(self.game.guessed_letters))
                        if self.game.guessed_letters else 'None')
        self.guessed_label.config(text=f"Guessed letters: {guessed_text}")

    def game_over(self, message):
        """Handle game over"""
        # Stop timer
        self.stop_timer()

        answer = self.game.get_answer() if self.game else "Unknown"

        result = messagebox.askyesno("Game Over",
                                     f"{message}\n\nCorrect answer: {answer}\n\nPlay again?")

        if result:
            self.new_game()
        else:
            self.show_main_menu()

    def new_game(self):
        """Start new game"""
        # Stop any running timer
        self.stop_timer()
        self.show_main_menu()

    def run(self):
        """Start GUI main loop"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        print("Starting Hangman game...")
        app = HangmanGUI()
        app.run()
    except (ImportError, AttributeError, RuntimeError, tk.TclError) as e:
        print(f"Error starting game: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
        sys.exit(0)
    except SystemExit as e:
        sys.exit(e.code if e.code is not None else 0)
    except (ValueError, TypeError, OSError) as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
    except Exception as e:
        # Log the unexpected error for debugging
        print(f"Critical error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
