import random
import tkinter as tk

def read_words(filename):
    with open(filename, 'r') as file:
        words = file.read().split()
    return words

def get_word(words):
    return random.choice(words)

def check_guess(guess, word):
    guess = guess.lower()
    word = word.lower()
    if len(guess) != len(word):
        return False
    for i in range(len(guess)):
        if guess[i] != word[i] and guess[i] in word:
            print(f"{guess[i]} is a correct letter, but it's in the wrong position.")
        elif guess[i] != word[i]:
            print(f"{guess[i]} is not in the word.")
        else:
            print(f"{guess[i]} is a correct letter in the correct position.")
    return guess == word

def main():
    words = read_words("words.txt")
    word = get_word(words)
    guesses = 0
    while guesses < 6:
        guess = input("Enter a five-letter guess: ")
        if guess == "e": #Exit shortcut TODO: remove
            break
        if check_guess(guess, word):
            print(f"Congratulations! You guessed the word '{word}' in {guesses + 1} guesses!")
            break
        else:
            guesses += 1
            print(f"Sorry, that guess is incorrect. You have {6 - guesses} guesses remaining.")
    else:
        print(f"Sorry, you didn't guess the word '{word}'. The word was '{word}'. Better luck next time!")
    
if __name__ == "__main__":
    main()
