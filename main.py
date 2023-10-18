from tkinter import *
from PIL import Image, ImageTk

# ---------------------------- CONSTANTS ------------------------------- #
WHITE = "#f8f8f8"
GREY = "#EEEEEE"
DARK = "#393E46"
DARK_GREY = "#929AAB"

FONT_NAME = "Courier"

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Study time")
window.config(padx=100, pady=50, bg=WHITE)

timer = Label(text="Timer", font=(FONT_NAME, 45), bg=WHITE, fg=DARK)
timer.grid(column=0, row=0)

timer = Label(text="Press left button to start and stop timer.", font=(FONT_NAME, 20), bg=WHITE, fg=DARK)
timer.grid(column=0, row=1, pady=25)

timer = Label(text="Press right button to switch between current time and day time.", font=(FONT_NAME, 20), bg=WHITE, fg=DARK)
timer.grid(column=0, row=2)

canvas = Canvas(width=395, height=675, bg=WHITE, highlightthickness=0)
watch_img = PhotoImage(file="watch_img.png")
canvas.create_image(197, 337, image=watch_img)
timer_text = canvas.create_text(197, 337, text="00:00", fill=GREY, font=(FONT_NAME, 45, "bold"))
canvas.grid(column=0, row=3, pady=25)

# Buttons
start_button = PhotoImage(file="button.png")
button_1 = Button(canvas, image=start_button, highlightthickness=0)
button_1_window = canvas.create_window(120, 470, anchor=CENTER, window=button_1)

button_2 = Button(canvas, image=start_button, highlightthickness=0)
button_2_window = canvas.create_window(265, 470, anchor=CENTER, window=button_2)




window.mainloop()
