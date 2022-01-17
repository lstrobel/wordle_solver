# Functions to simulate the Wordle game
import multiprocessing
import threading
import ray as ray
import random
import time
from itertools import repeat
import pandas as pd
from tqdm import tqdm
import guess_strategies
import solver
from util import get_result_string


@ray.remote
def run_solver(solution, guesser):
    """
    Runs the solver on the given solution
    """
    num_guesses = [0]
    solver.main(
        lambda g, s=solution, u=num_guesses: get_result_string(g, s, u),
        lambda w: guesser.remote(w),
        False,
    )
    return num_guesses[0]


def run_game(guesser, parallel=True):
    """
    Uses the solver to run a game of Wordle. Returns how many guesses the solver took to get the solution
    """

    # Generate a random word from the available dataset
    with open("res/official.txt", "r") as f:
        words = f.read().splitlines()

    # duplicate_words the words, so we run each entry three times and shuffle
    words = [word for word in words for _ in range(3)]
    random.shuffle(words)

    # Run everything
    if parallel:
        with multiprocessing.Pool() as pool:
            data = pool.starmap(run_solver, zip(words, repeat(guesser)))
    else:
        data = []
        # for word in tqdm(words):
        #     data.append(run_solver(word, guesser))
        for word in tqdm(words):
            data.append(run_solver.remote(word, guesser))
        data = [d.get() for d in data]
    return pd.Series(data)


if __name__ == "__main__":
    start_time = time.time()
    s = run_game(guess_strategies.guess_bruteforce, False)

    duration = time.time() - start_time
    # Pretty print duration
    print(f"Duration: {duration}s")
    print(s.describe())
