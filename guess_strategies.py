import random
from functools import reduce


def guess_random(words):
    """
    Choose a random word

    Results:
        count    2315.000000
        mean        4.488553
        std         1.041998
        min         2.000000
        25%         4.000000
        50%         4.000000
        75%         5.000000
        max        10.000000
        dtype: float64
    """

    return random.choice(list(words))


def guess_sum_frequencies(words):
    """
    Choose a word based on the sum of positional letter frequencies

    Results:
        count    2315.000000
        mean        4.040173
        std         0.863968
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
        count    2315.000000
        mean        4.252268
        std         0.942760
        min         2.000000
        25%         4.000000
        50%         4.000000
        75%         5.000000
        max         8.000000
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


if __name__ == "__main__":
    with open("res/official.txt", "r") as f:
        # Ingest lines into a set without whitespace
        words = set(f.read().split())
        guess_basic_markov(words)
