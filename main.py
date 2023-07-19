import curses
import random
import time
from curses import wrapper


# Class that manages the SpeedTypingTest game
class SpeedTypingTest:
    """A class that represents the speed typing test game."""

    # Initialize the class with the screen object
    def __init__(self, stdscr):
        """Constructor method to initialize the game screen."""
        self.stdscr = stdscr  # the screen object

    # Clears and sets up the start screen
    def _start_screen(self):
        """Private method to set up the start screen and wait for user input to begin."""
        self.stdscr.clear()  # clear the screen
        # welcome message
        self.stdscr.addstr("Welcome to the Speed Typing Test!\nPress any key to begin!")
        self.stdscr.refresh()  # refresh to display message
        self.stdscr.getkey()  # wait for key press

    # Displays the typing test text, the current text, and the calculated WPM
    def _display_text(self, target, current, wpm=0):
        """Private method to display target text, current text and calculated WPM on the screen."""
        self.stdscr.addstr(target)  # add the target text to screen
        # add the words per minute (WPM) to screen
        self.stdscr.addstr(5, 0, f"WPM: {wpm}")

        # color the user's typing, green for correct and red for incorrect
        for i, char in enumerate(current):
            correct_char = target[i]
            color = curses.color_pair(1) if char == correct_char else curses.color_pair(2)
            self.stdscr.addstr(0, i, char, color)

    # Loads a random line from the text file for the user to type
    def _load_text(self):
        """Private method to load a random line from the text file for the user to type."""
        with open("text_sample.txt", "r") as f:
            return random.choice(f.readlines()).strip()

    # Manages the words per minute test
    def _wpm_test(self):
        """Private method to manage the WPM test until the user completes typing the target text."""
        target_text = self._load_text()  # load the target text
        current_text, wpm = [], 0  # initialize current text and WPM
        start_time = time.time()  # record start time
        self.stdscr.nodelay(True)  # make input non-blocking

        # loop until the user types the complete target text
        while "".join(current_text) != target_text:
            time_elapsed = max(time.time() - start_time, 1)  # calculate elapsed time
            wpm = round((len(current_text) / (time_elapsed / 60)) / 5)  # calculate WPM
            self.stdscr.clear()  # clear the screen
            # display the target text, current text, and WPM
            self._display_text(target_text, current_text, wpm)
            self.stdscr.refresh()  # refresh the screen

            # handle key presses from the user
            try:
                key = self.stdscr.getkey()  # get the key pressed by the user
                if ord(key) == 27: break  # if ESC key is pressed, break
                if key in ("KEY_BACKSPACE", '\b', "\x7f") and current_text:  # handle backspace
                    current_text.pop()
                elif len(current_text) < len(target_text):  # handle other keys
                    current_text.append(key)
            except:
                continue

        self.stdscr.nodelay(False)  # revert input to blocking

    # Main loop of the game
    def _main(self):
        """Main method to run the game loop until user decides to exit."""
        # initialize color pairs for the text
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

        # game loop
        self._start_screen()
        while True:
            self._wpm_test()  # start the WPM test
            # display completion message
            self.stdscr.addstr(2, 0, "You completed the text! Press any key to continue...")
            # if ESC key is pressed, break
            if ord(self.stdscr.getkey()) == 27:
                break


# start the game
def main(stdscr):
    game = SpeedTypingTest(stdscr)  # Create an instance of the game
    game._main()  # Call the instance method


wrapper(main)  # Pass the function to the wrapper
