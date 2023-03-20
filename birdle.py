import random
import tkinter as tk

def read_birds(filename):
    with open(filename, 'r') as file:
        birds = file.read().split()
    return birds

def get_bird(birds):
    return random.choice(birds)

def check_guess(guess, bird):
    guess = guess.lower()
    bird = bird.lower()
    return guess == bird

def main():
    birds = read_birds("birds.txt")
    bird = get_bird(birds)
    
    win = tk.Tk()
    win.title("Birdle")
    win.geometry("480x600")

    mf = tk.Frame(win) # main frame
    mf.pack(fill="both", padx=10, pady=10)
    
    title = tk.Label(mf, text="Birdle")
    title.pack()
    
    def handle_submission(event):
        text = entry.get()
        if text:
            if check_guess(text, bird):
                print("Correct!")
                entry.config(state="disabled")
            else:
                print("Incorrect!")
                entry.delete(0, tk.END)

    entry = tk.Entry(mf)
    entry.pack()
    entry.bind('<Return>', handle_submission)

    submit = tk.Button(mf, text="Submit")
    submit.pack()
    submit.bind("<Button-1>", handle_submission)
    
    win.mainloop()
    
    # guesses = 0
    # while guesses < 6:
    #     guess = input("Enter a five-letter guess: ")
    #     if guess == "e": #Exit shortcut TODO: remove
    #         break
    #     if check_guess(guess, word):
    #         print(f"Congratulations! You guessed the word '{word}' in {guesses + 1} guesses!")
    #         break
    #     else:
    #         guesses += 1
    #         print(f"Sorry, that guess is incorrect. You have {6 - guesses} guesses remaining.")
    # else:
    #     print(f"Sorry, you didn't guess the word '{word}'. The word was '{word}'. Better luck next time!")
    
if __name__ == "__main__":
    main()
