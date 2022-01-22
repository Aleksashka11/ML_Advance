import random
import os


"""Menu for the game."""


def options():
    menu_options = {
        1: "Start",
        2: "See previous words",
        3: "Exit"
    }
    for key in menu_options.keys():
        print(key, '-', menu_options[key])


"""Function to get random word."""


def get_word():
    words = ['code', 'python', 'flask']
    chosen_word = random.choice(words)
    return chosen_word


"""Results of the game."""


def results(missedLetters, guessedLetters, randomWord):
    print("Missed Letters: " + missedLetters)
    output = "*" * len(randomWord)
    for i in range(len(guessedLetters)):
        if guessedLetters[i] in randomWord:
            pos = randomWord.find(guessedLetters[i])
            output = output[:pos] + guessedLetters[i] + output[pos + 1:]
    for j in range(len(output)):
        print(output[j])


"""Function for guessing letters."""


def guess(typedLetters):
    print("Type a letter: ")
    letter = input()
    if len(letter.lower()) != 1:
        print("You need to enter 1 letter")
    elif letter.lower() in typedLetters:
        print("You have already entered this letter")
    elif letter.lower().isalpha() is False:
        print("You need to enter a letter")
    else:
        return letter


"""Getting file path."""


def filePath():
    file_path = os.path.join(os.path.expanduser('~'), 'previous.txt')
    return file_path


"""Writing previous word to file."""


def previousWords(word):
    file_path = filePath()
    with open(file_path, 'a+') as f:
        f.write(word)
        f.write('\n')


"""Function to print attempts."""


def attemptsNumber(attempts):
    fixed_number_attempts = 10
    used_attempts = fixed_number_attempts - attempts
    print("Number of used attempts: " + str(used_attempts))
    print("Number of attempts that left: " + str(attempts))


file_path = filePath()
file = open(file_path, 'w+')
file.truncate(0)
finish = False
while finish is False:
    options()
    option = int(input('Enter your choice: '))
    if option == 1:
        missedLetters = ""
        guessedLetters = ""
        typedLetters = missedLetters + guessedLetters
        word = get_word()
        previousWords(word)
        attempts = 10
        used_attempts = 0
        end = False
        while end is False:
            guessedLetter = guess(typedLetters)
            if guessedLetter in word and attempts != 0:
                guessedLetters = guessedLetters + guessedLetter
                results(missedLetters, guessedLetters, word)
                attemptsNumber(attempts)
            if guessedLetter not in word and attempts != 0:
                missedLetters = missedLetters + guessedLetter
                results(missedLetters, guessedLetters, word)
                attempts = attempts - 1
                attemptsNumber(attempts)
            if len(guessedLetters) == len(word) and attempts != 0:
                print("You win. The secret word is " + word)
                end = True
            if attempts == 0:
                print("You failed. The secret word was " + word)
                end = True
    elif option == 2:
        print("List of previously used words: ")
        file_path = filePath()
        with open(file_path, 'r') as reader:
            print(reader.read())
    elif option == 3:
        print('Exiting the game')
        finish = True
        exit()
    else:
        print('Invalid option. Please enter a number between 1 and 3.')