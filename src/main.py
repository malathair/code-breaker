#!/usr/bin/env python3

import json
import os
import random


def clear() -> None:
    print("\033c", end="")


class CodeBreaker:
    def __init__(self) -> None:
        self.__difficulty: dict = None
        self.__secret_code: str = None
        self.__history: list = []

        self.__last_guess_invalid: bool = False
        self.__player_has_won: bool = False
        self.play_again: bool = False

        self.__board_header: str = None
        self.__board_footer: str = None
        self.__board_previous_guess: str = None

        self.__set_difficulty()
        self.__gen_code()
        self.__set_board_header()
        self.__set_board_previous_guess_format()
        self.__set_board_footer_format()

    def __check_guess(self, guess: str) -> None:
        if guess == self.__secret_code:
            self.__player_has_won = True

        clues = {}
        for index, num in enumerate(guess):
            if num not in self.__secret_code:
                continue

            if num not in clues:
                clues[num] = ""

            if num == self.__secret_code[index]:
                clues[num] = "\033[32mc"
            else:
                if not clues[num]:
                    clues[num] = "\033[33mw"

        return "".join(sorted([clue for _, clue in clues.items() if clue])) + "\033[39m"

    def __display_game_end(self) -> None:
        clear()
        self.__draw_board(True)

        if self.__player_has_won:
            message = "Game Won!"
        else:
            message = "Game Lost!"

        print(f"  {message}", "\n")

        self.play_again = True if input("  Would you like to play again? [y/N]: ").lower() == "y" else False

    def __draw_board(self, display_code: bool = False) -> None:
        if display_code:
            code = self.__secret_code
        else:
            code = "*" * len(self.__secret_code)
        print(
            self.__board_header.format(self.__difficulty["name"].ljust(30), code.ljust(20)),
            end="",
        )

        if len(self.__history) > 0:
            for guess, clue in self.__history:
                clue_length = int((len(clue) - 5) / 6)
                print(
                    self.__board_previous_guess.format(guess.center(24), clue.ljust(len(clue) + 5 - clue_length)),
                    end="",
                )

        print(self.__board_footer.format(str(self.__difficulty["max_guesses"] - len(self.__history)).ljust(19)))

    # Generate a random code. The length of which is determined by the game difficulty
    def __gen_code(self) -> None:
        number = str(random.randint(0, 10 ** self.__difficulty["code_len"] - 1))
        self.__secret_code = number.zfill(self.__difficulty["code_len"])
        if len(self.__secret_code) != self.__difficulty["code_len"]:
            raise ValueError("Generated secret code is not the correct length!")

    def __load_difficulty_settings(self) -> dict:
        filename = "levels.json"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(filepath) as file:
            difficulty_settings = json.load(file)

        for level in difficulty_settings:
            difficulty_settings[level]["name"] = difficulty_settings[level]["name"].replace(r"\u001b", "\033")

        return difficulty_settings

    def __make_guess(self) -> None:
        if self.__last_guess_invalid:
            print("  \033[31mYou entered an invalid or duplicate guess!\033[39m", "\n")
        guess = input("  Please make a guess> ")

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

    def __set_board_footer_format(self) -> None:
        filename = "assets/board_footer.txt"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(filepath) as file:
            self.__board_footer = file.read()

    def __set_board_header(self) -> None:
        filename = "assets/board_header.txt"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(filepath) as file:
            self.__board_header = file.read()

    def __set_board_previous_guess_format(self) -> None:
        filename = "assets/previous_guess.txt"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(filepath) as file:
            self.__board_previous_guess = file.read()

    # Set game difficulty. Determines the length of the code to break
    def __set_difficulty(self) -> None:
        difficulty_settings = self.__load_difficulty_settings()
        difficulty_is_set = False
        invalid_choice = False

        filename = "assets/difficulty_menu.txt"
        filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
        with open(filepath) as file:
            difficulty_menu = file.read()
            difficulty_menu.replace("\\033", "\033")

        while not difficulty_is_set:
            clear()
            print(difficulty_menu)

            if invalid_choice:
                print("  \033[31mInvalid selection! Please select a valid difficulty\033[39m", "\n")
                invalid_choice = False

            choice = input("  > ")

            try:
                int(choice)
                if int(choice) < 1 or int(choice) > 3:
                    raise ValueError("Difficulty level must be between 1 and 3")
                self.__difficulty = difficulty_settings[choice]
            except ValueError:
                invalid_choice = True
            else:
                difficulty_is_set = True
            finally:
                pass

    def run(self) -> None:
        while len(self.__history) < self.__difficulty["max_guesses"] and not self.__player_has_won:
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
