import json
import random
import tkinter as tk

def get_bird_data():
    with open('birds.json', 'r') as file:
        bird_data = random.choice(json.load(file)['species'])
    return bird_data

def check_guess(guess, bird):
    guess = guess.lower()
    bird = bird.lower()
    return guess == bird

def main():
    bird_data = get_bird_data()
    bird = bird_data['common_name']
    
    win = tk.Tk()
    win.title("Birdle")
    win.geometry("480x600")

    mf = tk.Frame(win) # main frame
    mf.pack(fill="both", padx=10, pady=10)
    
    tk.Label(mf, text="Birdle").pack()

    hf = tk.Frame(mf) # hint frame
    hf.pack()

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
            submitEntry.delete(0, tk.END)
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
                disable()

    submitEntry.bind('<Return>', handle_submission)
    submitBtn.bind("<Button-1>", handle_submission)
    
    win.mainloop()
    
if __name__ == "__main__":
    main()
