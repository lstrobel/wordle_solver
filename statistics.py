# Calculate some interesting statistics about the dataset to inform our first word choice
from functools import reduce

# create set
lines = None

# Open file
with open("res/official.txt", "r") as f:
    # Ingest lines into a set without whitespace
    lines = set(f.read().split())

print("Number of unique words:", len(lines))

# calculate frequency of each letter by position
# create a list of maps, where each index in the list is a position, and the maps are the frequencies of each letter
freq_by_pos = [{} for _ in range(5)]
for word in lines:
    for i in range(len(word)):
        if word[i] not in freq_by_pos[i]:
            freq_by_pos[i][word[i]] = 1
        else:
            freq_by_pos[i][word[i]] += 1

# print out the frequencies
print("Frequencies by position:")

for i in range(5):
    print(freq_by_pos[i])

# print the most common letter in each position
print("Most common letter in each position:")

for i in range(5):
    print(max(freq_by_pos[i], key=freq_by_pos[i].get))

# Get the product of the probabilities of each letter in each position for each word
word_probabilities = {}
for word in lines:
    prob = [0 for _ in range(5)]
    for i in range(len(word)):
        prob[i] = freq_by_pos[i][word[i]] / len(lines)
    word_probabilities[word] = reduce(lambda x, y: x * y, prob)

# Print the top 5 words and their probabilities
top_five = sorted(word_probabilities, key=word_probabilities.get, reverse=True)[:5]
print("Top 5 words and their probabilities:", top_five)
