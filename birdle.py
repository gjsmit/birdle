import json
import random
import tkinter as tk
from PIL import Image,ImageTk

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

    ohf = tk.Frame(mf) # outer hint frame
    ohf.pack()

    pc = tk.Canvas(ohf, width=100, height=100) # picture canvas
    pc.pack()

    # display image
    imgDir = "images/"
    try:
        img = ImageTk.PhotoImage(Image.open(imgDir+bird_data['picture']).resize((100,100), Image.ANTIALIAS))
    except:
        img = ImageTk.PhotoImage(Image.open(imgDir+"stock.png").resize((100,100), Image.ANTIALIAS))
    pc.create_image(0,0, anchor=tk.NW, image=img)

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
    tk.Label(thf, text=bird_data['habitat']).grid(row=1, column=1, sticky="w")
    tk.Label(thf, text=bird_data['diet']).grid(row=2, column=1, sticky="w")
    tk.Label(thf, text=bird_data['length']).grid(row=3, column=1, sticky="w")
    tk.Label(thf, text=bird_data['wingspan']).grid(row=4, column=1, sticky="w")

    # ihf = tk.Frame(ohf) # inner hint frame
    # ihf.pack()

    # bf = tk.Frame(ohf) # button frame
    # bf.pack()

    # # buttons to switch between hints
    # btn1 = tk.Button(bf, text="1")
    # btn2 = tk.Button(bf, text="2")
    # btn3 = tk.Button(bf, text="3")
    # btn4 = tk.Button(bf, text="4")
    # btn5 = tk.Button(bf, text="5")
    # btn6 = tk.Button(bf, text="6")
    # btn1.grid(column=0, row=0)
    # btn2.grid(column=1, row=0)
    # btn3.grid(column=2, row=0)
    # btn4.grid(column=3, row=0)
    # btn5.grid(column=4, row=0)
    # btn6.grid(column=5, row=0)

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
