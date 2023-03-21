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
    
    tk.Label(mf, text="Birdle").pack()

    sf = tk.Frame(mf) # submissions frame
    sf.pack()

    submitEntry = tk.Entry(sf)
    submitEntry.grid(row=6, column=0, padx=2)

    submitBtn = tk.Button(sf, text="Submit")
    submitBtn.grid(row=6, column=1, padx=2)

    remGuesses = 6
    remLbl = tk.Label(mf, text="You have 6 guesses remaining.")
    remLbl.pack()

    def handle_submission(event):
        nonlocal remGuesses
        guess = submitEntry.get()

        def log_guess(isCorrect):
            nonlocal remGuesses, guess

            tk.Label(sf, text=guess).grid(row=6-remGuesses, column=0, sticky="w", ipadx=1)
            tk.Label(sf, text=(u'\u2713' if isCorrect else "X")).grid(row=6-remGuesses, column=1)

        def disable():
            submitEntry.config(state="disabled")
            submitBtn.config(state="disabled")

        if guess:
            if check_guess(guess, bird):
                log_guess(True)
                remLbl.config(text="Correct!")
                disable()
            elif remGuesses > 1:
                log_guess(False)
                remGuesses -= 1
                remLbl.config(text="Incorrect! You have {} guesses remaining.".format(remGuesses))
                submitEntry.delete(0, tk.END)
            else:
                log_guess(False)
                remLbl.config(text="Incorrect! Better luck next time!")
                submitEntry.delete(0, tk.END)
                disable()

    submitEntry.bind('<Return>', handle_submission)
    submitBtn.bind("<Button-1>", handle_submission)
    
    win.mainloop()
    
if __name__ == "__main__":
    main()
