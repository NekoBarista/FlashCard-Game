import random
import tkinter
import pandas

BACKGROUND_COLOR = "#B1DDC6"


# ----- Load Words ---------
try:
    french_df = pandas.read_csv("./data/words_to_learn.csv")
    french_dictionary = french_df.to_dict("records")

except FileNotFoundError:
    french_df = pandas.read_csv("./data/french_words.csv")
    french_dictionary = french_df.to_dict("records")


# ----- Create Window ---------
window = tkinter.Tk()
window.title("Learn French with Flashcards!")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
# Create UI
canvas = tkinter.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front = tkinter.PhotoImage(file="./images/card_front.png")
card = canvas.create_image(400, 263, image=card_front)
Heading = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
Word = canvas.create_text(400, 263, text="trouve", font=("ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)


# ------------Flip Card --------

word = {}

def flip_card():
    english_word = word["English"]
    canvas.itemconfig(card, image=card_back)
    canvas.itemconfig(Heading, text="English", fill="white")
    canvas.itemconfig(Word, text=english_word, fill="white")


# ----- Load New French Word -----

flip_timer = window.after(3000, flip_card)

def load_french_word():
    global word
    global flip_timer
    window.after_cancel(flip_timer)
    canvas.itemconfig(card, image=card_front)
    canvas.itemconfig(Heading, text="French", fill="black")
    word = french_dictionary[random.randint(0, len(french_dictionary))]
    french_word = word["French"]
    canvas.itemconfig(Word, text=french_word, fill='black')
    flip_timer = window.after(3000, flip_card)

def known_word():
    french_dictionary.remove(word)
    load_french_word()
    word_list = pandas.DataFrame(french_dictionary)
    word_list.to_csv("./data/words_to_learn.csv", index=False)
# ---- buttons -----


wrong_image = tkinter.PhotoImage(file="./images/wrong.png")
wrong_button = tkinter.Button(image=wrong_image, background=BACKGROUND_COLOR,
                              highlightthickness=0, bd=0, compound="center", command=load_french_word)
wrong_button.grid(column=0, row=1)

right_image = tkinter.PhotoImage(file="./images/right.png")
right_button = tkinter.Button(image=right_image, background=BACKGROUND_COLOR,
                              highlightthickness=0, bd=0, compound="center", command=known_word)
right_button.grid(column=1, row=1)

# --- Flip Cards ----
card_back = tkinter.PhotoImage(file="./images/card_back.png")

load_french_word()

window.mainloop()
