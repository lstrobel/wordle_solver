# Functions to simulate the Wordle game
import multiprocessing
import time

import pandas as pd

import guess_strategies as gs
import solver


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


def run_solver(solution):
    """
    Runs the solver on the given solution
    """
    num_guesses = [0]
    solver.main(lambda g, s=solution, u=num_guesses: get_result_string(g, s, u), gs.guess_random, False)
    return num_guesses[0]


def run_game():
    """
    Uses the solver to run a game of Wordle. Returns how many guesses the solver took to get the solution
    """

    # Generate a random word from the available dataset
    with open("res/official.txt", "r") as f:
        words = f.read().splitlines()

    # Initialize the solver
    start_time = time.time()

    with multiprocessing.Pool() as pool:
        data = pool.map(run_solver, words)

    duration = time.time() - start_time
    # Pretty print duration and results
    print(f"{len(words)} words took {duration} seconds to solve")
    s = pd.Series(data)
    print(s.describe())


if __name__ == "__main__":
    run_game()
