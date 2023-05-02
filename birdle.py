import json
import random
import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk

def get_bird():
    with open('birds.json', 'r') as file:
        bird_data = random.choice(json.load(file)['species'])
    return bird_data

def get_bird_names():
    with open('birds.json', 'r') as file:
        bird_names = [bird['common_name'] for bird in json.load(file)['species']]
    return bird_names

def check_guess(guess, bird):
    guess = guess.lower()
    bird = bird.lower()
    return guess == bird

def main():

    bird_data = get_bird()
    bird = bird_data['common_name']
    bird_names = get_bird_names()
    
    win = tk.Tk()
    win.title("Birdle")
    win.geometry("480x600")
    win.iconbitmap("images/logo.ico")

    mf = tk.Frame(win) # main frame
    mf.pack(fill="both", padx=10, pady=10)
    
    tk.Label(mf, text="Birdle", font="bold").pack()

    ohf = tk.Frame(mf, pady=30) # outer hint frame
    ohf.pack()

    pc = tk.Canvas(ohf, width=150, height=150) # picture canvas
    pc.pack()

    # display image
    try:
        img = ImageTk.PhotoImage(Image.open("images/birds/"+bird_data['picture']).resize((150,150), Image.LANCZOS))
    except:
        img = ImageTk.PhotoImage(Image.open("images/stock.png").resize((150,150), Image.LANCZOS))
    preimg = ImageTk.PhotoImage(Image.open("images/unknown.png").resize((150,150), Image.LANCZOS)) # TODO: set to unknown
    pc.create_image(0,0, anchor=tk.NW, image=preimg)

    cf = tk.Frame(ohf)  # song/call frame
    cf.pack()

    thf = tk.Frame(ohf) # text hints frame
    thf.pack()

    tk.Label(thf, text="Scientific Name:").grid(row=0, column=0, sticky="e")
    tk.Label(thf, text="Habitat:").grid(row=1, column=0, sticky="e")
    tk.Label(thf, text="Diet:").grid(row=2, column=0, sticky="e")
    tk.Label(thf, text="Length:").grid(row=3, column=0, sticky="e")
    tk.Label(thf, text="Wingspan:").grid(row=4, column=0, sticky="e")

    tk.Label(thf, text=bird_data['scientific_name']).grid(row=0, column=1, sticky="w")

    sf = tk.Frame(mf) # submissions frame
    sf.pack()

    guess = tk.StringVar()

    submitEntry = ttk.Combobox(sf, textvariable=guess, height=10, width=len(max(bird_names, key=len))+3)
    submitEntry['values'] = bird_names
    submitEntry.grid(row=6, column=0, padx=2)

    def get_autofill(event):
        keys = event.widget.get()
        if keys == '': data = bird_names
        else:
            data = []
            for item in bird_names:
                if keys.lower() in item.lower():
                    data.append(item)
        submitEntry['values'] = data

    submitEntry.bind('<KeyRelease>', get_autofill)

    submitBtn = tk.Button(sf, text="Submit")
    submitBtn.grid(row=6, column=1, padx=2)

    remGuesses = 6
    remLbl = tk.Label(mf, text="You have 6 guesses remaining.")
    remLbl.pack()

    def handle_submission(event):
        nonlocal remGuesses, guess

        def log_guess(isCorrect):
            nonlocal remGuesses, guess
            adj_guess = guess.get()
            if adj_guess == "": adj_guess = "skipped..."
            
            tk.Label(sf, text=adj_guess).grid(row=6-remGuesses, column=0, sticky="w", ipadx=1)
            tk.Label(sf, text=(u'\u2713' if isCorrect else "X")).grid(row=6-remGuesses, column=1)

        def show_hint():
            nonlocal remGuesses
            
            if remGuesses == 6:
                tk.Label(thf, text=bird_data['habitat']).grid(row=1, column=1, sticky="w")
            elif remGuesses == 5:
                tk.Label(thf, text=bird_data['diet']).grid(row=2, column=1, sticky="w")
            elif remGuesses == 4:
                tk.Label(thf, text=bird_data['length']).grid(row=3, column=1, sticky="w")
                tk.Label(thf, text=bird_data['wingspan']).grid(row=4, column=1, sticky="w")
            elif remGuesses == 3:
                tk.Label(cf, text="MP3 player coming soon...").pack()
            else:
                pc.create_image(0,0, anchor=tk.NW, image=img)

        def disable():
            submitEntry.delete(0, tk.END)
            submitEntry.insert(0, bird_data['common_name'])
            submitEntry.config(state="disabled")
            submitBtn.config(state="disabled")

        submitEntry['values'] = bird_names
        
        if remGuesses < 1:
            return
        elif guess.get() not in bird_names:
            submitEntry.event_generate('<KeyRelease>')
            submitEntry.event_generate('<Down>')
        elif check_guess(guess.get(), bird):
            log_guess(True)
            while remGuesses > 1:
                show_hint()
                remGuesses -= 1
            remLbl.config(text="Correct!")
            disable()
        elif remGuesses > 1:
            log_guess(False)
            show_hint()
            bird_names.remove(guess.get())
            remGuesses -= 1
            remLbl.config(text="Incorrect! You have {} guess{} remaining.".format(remGuesses, "" if remGuesses == 1 else "es"))
            submitEntry.delete(0, tk.END)
        else:
            log_guess(False)
            remLbl.config(text="Incorrect! Better luck next time!")
            remGuesses -= 1
            disable()

    submitEntry.bind('<Return>', handle_submission)
    submitBtn.bind("<Button-1>", handle_submission)
    
    win.mainloop()
    
if __name__ == "__main__":
    main()
