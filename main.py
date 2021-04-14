from tkinter import *
import pandas
import random
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"
LANGUAGE_FONT = ("Arial", 40, "italic")
WORD_FONT = ("Arial", 60, "bold")
current_card = {}
try:
    data = pandas.read_csv('data/words_to_learn')
except FileNotFoundError:
    original_data = pandas.read_csv('data/french_words.csv')
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_image)
    canvas.itemconfig(card_title, text="English", fill='white')
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill='black')
    canvas.itemconfig(card_word, text=current_card['French'], fill='black')
    canvas.itemconfig(canvas_image, image=card_front_image)
    flip_timer = window.after(3000, flip_card)


def is_known():
    if len(to_learn) > 0:
        to_learn.remove(current_card)
        data = pandas.DataFrame(to_learn)
        data.to_csv('data/words_to_learn.csv', index=False)
        next_card()
    else:
        messagebox.showinfo(title="Congratulations!", message="You manage to learn all words!")


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

canvas = Canvas(width=800, height=525, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file='images/card_front.png')
card_back_image = PhotoImage(file='images/card_back.png')
canvas_image = canvas.create_image(400, 262, image=card_front_image)
canvas.grid(row=0, column=0, columnspan=2)

check_image = PhotoImage(file='images/right.png')
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)

cross_image = PhotoImage(file='images/wrong.png')
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

card_title = canvas.create_text(400, 150, text='Title', font=LANGUAGE_FONT)
card_word = canvas.create_text(400, 263, text='word', font=WORD_FONT)
next_card()

window.mainloop()
