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
