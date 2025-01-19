#!/usr/bin/env python3

import enum
import random


MAX_GUESSES = 10


BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
DEFAULT = "\033[38m"
RESET = "\033[39m"


def clear() -> None:
    print("\033c", end="")


class CodeBreaker:
    def __init__(self) -> None:
        self.__difficulty: int = None
        self.__secret_code: str = None
        self.__history: list = []

        self.__last_guess_invalid = False
        self.__player_has_won = False
        self.play_again = False

        self.__set_difficulty()
        self.__gen_code()

    def __check_guess(self, guess: str) -> None:
        if guess == self.__secret_code:
            self.__player_has_won = True
            return GREEN + "ccc" + RESET

        clues = {}
        for index, num in enumerate(guess):
            if num not in self.__secret_code:
                continue

            if num not in clues:
                clues[num] = ""

            if num == self.__secret_code[index]:
                clues[num] = GREEN + "c"
            else:
                if not clues[num]:
                    clues[num] = YELLOW + "w"

        return "".join(sorted([clue for _, clue in clues.items() if clue])) + RESET

    def __display_game_end(self) -> None:
        if self.__player_has_won:
            print("\n", "Game Won!", "\n")
        else:
            print("Game Lost! The secret code was:", self.__secret_code, "\n")

        self.play_again = True if input("Would you like to play again? [y/N]: ").lower() == "y" else False

    # Generate a random code. The length of which is determined by the game difficulty
    def __gen_code(self) -> None:
        length = int(self.__difficulty) + 2
        number = str(random.randint(0, 10**length - 1))
        self.__secret_code = number.zfill(length - len(number))

    def __make_guess(self) -> None:
        if self.__last_guess_invalid:
            print(RED + "You entered an invalid or duplicate guess!" + RESET + "Please try again:")
        else:
            print("Please make a guess:")
        guess = input("> ")

        try:
            int(guess)
            if len(guess) != len(self.__secret_code):
                raise ValueError(
                    "The length of the entered code was",
                    len(guess),
                    "when it should have been",
                    len(self.__secret_code),
                )
            for record in self.__history:
                if guess == record[0]:
                    raise ValueError("This guess is a duplicate!")
        except ValueError:
            self.__last_guess_invalid = True
        else:
            self.__last_guess_invalid = False
            clue = self.__check_guess(guess)
            self.__history.append((guess, clue))
        finally:
            pass

    def __draw_board(self) -> None:
        print("A secret code has been set! Can you break it?", "\n")

        if len(self.__history) > 0:
            print("Previous guesses:")

            for guess, clue in self.__history:
                print(f"  {guess} - {clue}")

            print("")

        print("Remaining guesses:", MAX_GUESSES - len(self.__history), "\n")

    # Set game difficulty. Determines the length of the code to break
    def __set_difficulty(self) -> None:
        difficulty_set = False
        invalid_choice = False

        while not difficulty_set:
            clear()
            print("Please select a difficulty:", "\n")
            print("  1. " + GREEN + "Easy" + RESET + "   (3 digit code)")
            print("  2. " + YELLOW + "Medium" + RESET + " (4 digit code)")
            print("  3. " + RED + "Hard" + RESET + "   (5 digit code)", "\n")

            if invalid_choice:
                print(RED + "Invalid selection! Please select a valid difficulty:" + RESET)
                invalid_choice = False

            choice = input("> ")

            try:
                self.__difficulty = int(choice)
                if self.__difficulty < 1 or self.__difficulty > 3:
                    raise ValueError("Code length must be between 3 and 5")
            except ValueError:
                invalid_choice = True
            else:
                difficulty_set = True
            finally:
                pass

    def run(self) -> None:
        while len(self.__history) < MAX_GUESSES and not self.__player_has_won:
            clear()
            self.__draw_board()
            self.__make_guess()

        self.__display_game_end()


def main() -> None:
    while True:
        game = CodeBreaker()
        try:
            game.run()
        except KeyboardInterrupt:
            # Handle ^C gracefullly
            break
        else:
            if not game.play_again:
                break
        finally:
            clear()


if __name__ == "__main__":
    main()
