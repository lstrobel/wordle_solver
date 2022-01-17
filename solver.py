# Solve the game wordle, by reducing the possible words at each stage, and then choosing the most likely one
from typing import Callable

import guess_strategies as gs


def trim_word_space(words, possible_letters, known_letters):
    """
    Trim the word space by removing words that don't have the letters we know
    """
    valid_words = words.copy()
    for word in words:
        for i in range(len(word)):
            if word[i] not in possible_letters[i]:
                valid_words.remove(word)
                break

    for letter in known_letters:
        for word in valid_words.copy():
            if letter not in word:
                valid_words.remove(word)

    return valid_words


def query_result(guess):
    # For debug, use user input
    return input("Result: ")


def main(
    query_result_func: Callable[[str], str], guesser: Callable[[set], str], debug=False
):
    # Open file
    with open("res/official.txt", "r") as f:
        # Ingest lines into a set without whitespace
        valid_words = set(f.read().split())

    # Create an alphabet from the letters present in the word dataset
    alphabet = set()
    for word in valid_words:
        for letter in word:
            alphabet.add(letter)

    if debug:
        print("Number of unique words:", len(valid_words))
        print("Alphabet:", sorted(alphabet))

    # The letters that are allowed in each position. Starts with 5 sets that have the full alphabet
    possible_letters = [alphabet.copy() for _ in range(5)]

    # Collection of letters we know are in the word somewhere
    known_letters = set()

    # Main game loop
    # We take a guess, then we get the result back from the player
    # We then update the valid words based on the result
    # We then repeat until we have no more valid words, or we have won

    while len(valid_words) > 1:
        valid_words = trim_word_space(valid_words, possible_letters, known_letters)
        guess = guesser(valid_words)
        if debug:
            print("Number of valid words:", len(valid_words))
            if len(valid_words) < 20:
                print(valid_words)
            print("Guess:", guess)

        # Get the result of the guess as a specially formatted string
        # For each character in the string, "-" means the letter is not in the word,
        # "X" means the letter is in the word but the position is wrong,
        # and "O" means the letter is in the word and the position is correct
        result = query_result_func(guess)
        for i in range(len(guess)):
            if result[i] == "-":
                for letter_set in possible_letters:
                    if guess[i] in letter_set:
                        letter_set.remove(guess[i])
            elif result[i] == "X":
                possible_letters[i].remove(guess[i])
                known_letters.add(guess[i])
            elif result[i] == "O":
                possible_letters[i] = {guess[i]}


def get_result_string(guess, solution, output):
    """
    Resturns the result string for the given guess.
    For each character in the string, "-" means the letter is not in the word,
     "X" means the letter is in the word but the position is wrong,
    and "O" means the letter is in the word and the position is correct
    """
    result = ""
    for i in range(len(guess)):
        if guess[i] == solution[i]:
            result += "O"
        elif guess[i] in solution:
            result += "X"
        else:
            result += "-"

    output[0] += 1
    return result


if __name__ == "__main__":
    # main(query_result, debug=True)
    main(lambda g, s="solar", u=[0]: get_result_string(g, s, u), gs.guess_random, True)
