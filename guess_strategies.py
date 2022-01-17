import itertools
import random
from functools import reduce
from multiprocessing import Pool

import pandas as pd
import ray

import simulator


def guess_random(words):
    """
    Choose a random word

    Results:
        count    6945.000000
        mean        4.474730
        std         1.024598
        min         2.000000
        25%         4.000000
        50%         4.000000
        75%         5.000000
        max        11.000000
        dtype: float64
    """

    return random.choice(list(words))


def guess_sum_frequencies(words):
    """
    Choose a word based on the sum of positional letter frequencies

    Results:
        count    6945.000000
        mean        4.038877
        std         0.868641
        min         2.000000
        25%         3.000000
        50%         4.000000
        75%         4.000000
        max         8.000000
        dtype: float64
    """
    # calculate frequency of each letter by position
    freq_by_pos = [{} for _ in range(5)]
    for word in words:
        for i in range(len(word)):
            if word[i] not in freq_by_pos[i]:
                freq_by_pos[i][word[i]] = 1
            else:
                freq_by_pos[i][word[i]] += 1

    # Get the product of the probabilities of each letter in each position for each word
    word_probabilities = {}
    for word in words:
        prob = [0 for _ in range(5)]
        for i in range(len(word)):
            prob[i] = freq_by_pos[i][word[i]]
        word_probabilities[word] = reduce(lambda x, y: x + y, prob)

    # return most likely word
    return max(word_probabilities, key=word_probabilities.get)


def guess_basic_markov(words):
    """
    Guess using a simple "what is the most likely next letter" approach - similar to a typical markov chain

    Results:
        count    6945.000000
        mean        4.173218
        std         0.933150
        min         2.000000
        25%         4.000000
        50%         4.000000
        75%         5.000000
        max         9.000000
        dtype: float64
    """
    filtered_words = words.copy()
    for i in range(len(list(words)[0])):
        # Get most common next letter
        letters = [word[i] for word in filtered_words]
        most_common_letter = max(set(letters), key=letters.count)
        # remove words that do not have that letter at the desired position
        for word in filtered_words.copy():
            if word[i] != most_common_letter:
                filtered_words.remove(word)
    # return remaining element of filtered_words
    return list(filtered_words)[0]


@ray.remote
def _fix_start_guess(words: set, base_list: set, forced_guess: str):
    # If the passed words are equal to the base list, return the forced guess
    if words == base_list:
        return forced_guess

    return guess_sum_frequencies(words)


@ray.remote
def _run_with_words(solution_word, starting_word, words):
    # Get the number of steps to guess the solution word from the starting word
    count = ray.get(
        simulator.run_solver.remote(
            solution_word,
            lambda x: ray.get(_fix_start_guess.remote(x, words, starting_word)),
        )
    )
    return starting_word, count


@ray.remote
def guess_bruteforce(words):
    """
    Guess by testing each possible starting word, and calculating the average number of steps it takes
    guess_sum_frequencies() to guess it from there
    """
    if len(words) == 1:
        return list(words)[0]

    samples = random.sample(list(words), 2)
    out = []
    # params = itertools.product(
    #     samples,
    #     words,
    #     [words],
    #     [out],
    # )
    #
    # with Pool() as pool:
    #     # out = pool.starmap(
    #     #     _run_with_words, tqdm(params, total=len(words) * len(samples))
    #     # )
    #     out = pool.starmap(_run_with_words, params)
    for sample in samples:
        for word in words:
            out.append(_run_with_words.remote(sample, word, words))

    out = [ray.get(o) for o in out]
    df = pd.DataFrame(out, columns=["starting_word", "count"])

    # Group by starting word
    grouped = df.groupby("starting_word")

    # Return the starting word with the best average number of steps
    return grouped.mean().idxmin()["count"]


if __name__ == "__main__":
    with open("res/official.txt", "r") as f:
        # Ingest lines into a set without whitespace
        wordlist = set(f.read().split())
        print(ray.get(guess_bruteforce.remote(wordlist)))
