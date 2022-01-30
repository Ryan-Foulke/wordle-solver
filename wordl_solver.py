import numpy as np
from wordfreq import word_frequency

dictionary = np.loadtxt('5-letters.txt', dtype='str')


def get_user_input_2():
    # Data Structure
    unavailable = set()
    yellows = set()
    known = {0: [[], []], 1: [[], []], 2: [[], []], 3: [[], []], 4: [[], []]}

    # User Input
    guess = input("Enter guesses: ")
    guess_arr = []
    guess_arr = guess.split(",")
    color = input("Enter colors: ")
    color_arr = color.split(",")
    if(guess == ""):
        guess_arr = []

    # Data Input
    for x in range(len(guess_arr)):
        for y in range(5):
            letter = guess_arr[x][y]
            letter_color = int(color_arr[x][y])
            position = y
            if(letter_color == 0):
                if(letter not in yellows):
                    unavailable.add(letter)
                known[position][1].append(letter)
            if(letter_color == 1):
                yellows.add(letter)
                known[position][1].append(letter)
            if(letter_color == 2):
                if(letter in unavailable):
                    unavailable.remove(letter)
                yellows.add(letter)
                known[position][0].append(letter)
    return(unavailable, yellows, known)


def find_possibilities(unavailable, yellows, known):
    possibilities = []
    for word in dictionary:
        if(len(word) == 5):
            if(len(set(word) & set(unavailable)) == 0):
                if(len(yellows & set(word)) == len(yellows)):
                    possible = True
                    for position in range(5):
                        letter = word[position]
                        green = known[position][0]
                        yellow = known[position][1]
                        if((letter not in green) and (len(green) != 0)):
                            possible = False
                        if(letter in yellow):
                            possible = False
                    if(possible):
                        possibilities.append(word)
    return(possibilities)


def get_word_score(word, possibilities):
    letters = ''.join(possibilities)
    score = 0
    for letter in set(word):
        letter_score = letters.count(letter) / len(letters)
        score += letter_score
    return(score)


def best_guess(possibilities):
    best_word = ""
    best_score = 0
    for word in possibilities:
        score = 0
        if(len(possibilities) < 10):
            score = word_frequency(word, 'en')
        if(len(possibilities) >= 10):
            score = get_word_score(word, possibilities)
        if(score > best_score):
            best_word = word
            best_score = score
    return(best_word)


def print_instructions():
    print("")
    print("\033[95m WELCOME TO WORDLE SOVLER \033[0m")
    print("")
    print("\033[1m Instructions: \033[0m")
    print("Step 1: Enter the words you have guessed serperated by a comma.")
    print("Step 2: Enter the color code for the words serperated by a comma.")
    print("")
    print("\033[1m Color Code: \033[0m")
    print("0 = grey, 1 = yellow, 2 = green")
    print("Example: grey, grey, yellow, grey, green = 00102")
    print("")


if __name__ == "__main__":
    print_instructions()

    unavailable, yellows, known = get_user_input_2()
    possibilities = find_possibilities(unavailable, yellows, known)
    best_word = best_guess(possibilities)

    print("")

    if(len(possibilities) <= 25):
        print("REMAINING WORDS")
        print(possibilities)
        print("")

    print("There are \033[91m" + str(len(possibilities)) +
          "\033[0m possible words remaining.")
    print("The best word is \033[92m" + best_word + '\033[0m.')
