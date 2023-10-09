from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
# ---------------------------- FLIP CARD ------------------------------- #


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_image)


# ---------------------------- GENERATE NEW WORD ------------------------------- #
try:
    df = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_df = pandas.read_csv("data/french_words.csv")
    list_of_words = original_df.to_dict(orient="records")
else:
    list_of_words = df.to_dict(orient="records")


def generate_new_word_incorrect():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(list_of_words)
    canvas.itemconfig(canvas_image, image=card_front_image)
    canvas.itemconfig(language_text, text="French", fill="black")
    canvas.itemconfig(word_text, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, flip_card)


def generate_new_word_correct():
    list_of_words.remove(current_card)
    new_df = pandas.DataFrame(list_of_words)
    new_df.to_csv("data/words_to_learn.csv", index=False)
    generate_new_word_incorrect()


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(language_text, fill="white", text="English")
    canvas.itemconfig(word_text, fill="white", text=current_card["English"])


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flashcard App")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, flip_card)

card_back_image = PhotoImage(file="images/card_back.png")
card_front_image = PhotoImage(file="images/card_front.png")
canvas = Canvas(width=800, heigh=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front_image)
canvas.grid(row=0, column=0, columnspan=2)
language_text = canvas.create_text(
    400, 150, text="", fill="black", font=("Ariel", 40, "italic")
)
word_text = canvas.create_text(
    400, 263, text="", fill="black", font=("Ariel", 60, "bold")
)

check_image = PhotoImage(file="images/right.png")
check_button = Button(
    image=check_image, highlightthickness=0, command=generate_new_word_correct
)
check_button.grid(row=1, column=1)

x_image = PhotoImage(file="images/wrong.png")
x_button = Button(
    image=x_image, highlightthickness=0, command=generate_new_word_incorrect
)
x_button.grid(row=1, column=0)


generate_new_word_incorrect()


window.mainloop()
