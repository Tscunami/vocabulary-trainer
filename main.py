from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"
FONT_LANGUAGE = ("Ariel", 40, "italic")
FONT_WORD = ("Ariel", 60, "bold")

current_word = {}
flip_timer = 3000
to_learn = {}


def show_answer():
    canvas.itemconfig(card, image=back_image)
    canvas.itemconfig(language, fill="white", text="Czech")
    canvas.itemconfig(word, fill="white", text=current_word["Czech"])


def next_word():
    global current_word, flip_timer
    app.after_cancel(flip_timer)
    canvas.itemconfig(card, image=front_image)
    canvas.itemconfig(language, fill="black", text="English")
    current_word = choice(to_learn)
    selected_word = current_word["English"]
    canvas.itemconfig(word, fill="black", text=selected_word)
    flip_timer = app.after(3000, show_answer)


def remove_word():
    to_learn.remove(current_word)
    learned = pandas.DataFrame(to_learn)
    learned.to_csv("data/words_to_learn.csv", index=False)
    next_word()


try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/en_cs.csv")
finally:
    to_learn = data.to_dict(orient="records")


app = Tk()
app.title("Vocabulary Trainer")
app.config(padx=50, pady=50, bg="#B1DDC6")

canvas = Canvas(width=800, height=526, bg="#B1DDC6", highlightthickness=0)
front_image = PhotoImage(file="images/card_front.png")
back_image = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 263, image=front_image)
canvas.grid(row=0, column=0, columnspan=2)

language = canvas.create_text(400, 150, text="", font=FONT_LANGUAGE)
word = canvas.create_text(400, 263, text="", font=FONT_WORD)


no_image = PhotoImage(file="images/wrong.png")
no_button = Button(image=no_image, highlightthickness=0, command=next_word)
no_button.grid(row=1, column=0)

yes_image = PhotoImage(file="images/right.png")
yes_button = Button(image=yes_image, highlightthickness=0, command=remove_word)
yes_button.grid(row=1, column=1)

next_word()

app.mainloop()
