# This file takes the raw data from english.txt and creates a cleaned data source with valid wordle words

# Open the file
with open("res/google-10000-english-usa-no-swears-medium.txt", "r") as f:
    # Create output file
    with open("res/english_cleaned2.txt", "w") as f2:
        # read each line
        for line in f.readlines()[:5000]:
            line = line.strip()
            print(line)
            # must be five characters long, and contain only letters and starts with a lowercase letter
            if (
                len(line) == 5
                and line.isalpha()
                and line[0].islower()
            ):
                # write to file
                f2.write(line + "\n")
