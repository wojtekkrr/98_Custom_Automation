from tkinter import *
from datetime import datetime, timedelta
import math
import csv
import time
from random import randint

# ---------------------------- CONSTANTS ------------------------------- #
WHITE = "#f8f8f8"
GREY = "#EEEEEE"
DARK = "#393E46"
DARK_GREY = "#929AAB"

FONT_NAME = "Courier"

# ---------------------------- VARIABLES ------------------------------- #
status = "work"

mode = "now"

timer_r = None

clock_running = False


# ----------------------------- RUN ONCE DECORATOR ------------------------------- #
def run_once(func):
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            if clock_running is False:
                wrapper.has_run = True
            return func(*args, **kwargs)
    wrapper.has_run = False
    return wrapper


# ---------------------------------- SAVE DAY ------------------------------------ #
def save_day():
    now = datetime.now()
    with open("time.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now])


# ---------------------------------- SAVE DAY ------------------------------------ #
def save_time():
    now = datetime.now()
    with open("time.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now])


# ----------------------------- COUNTING MECHANISM ------------------------------- #
@run_once
def counting(seconds_overall):
    if clock_running:
        global timer_r
        godziny = seconds_overall // 60 // 60 % 60
        if godziny < 10:
            godziny = f"0{godziny}"
        minuty = seconds_overall // 60 % 60
        if minuty < 10:
            minuty = f"0{minuty}"
        sekundy = seconds_overall % 60
        if sekundy < 10:
            sekundy = f"0{sekundy}"

        canvas.itemconfig(timer_text, text=f"{godziny}:{minuty}")
        canvas.itemconfig(seconds_text, text=sekundy)

        if seconds_overall % 4 == 0 or seconds_overall % 4 == 1 or seconds_overall % 4 == 2:
            canvas.itemconfig(status_text, text=status)

        if seconds_overall % 4 == 3:
            canvas.itemconfig(status_text, text="")

        if seconds_overall % 4 == 0 or seconds_overall % 4 == 3 or seconds_overall % 4 == 2:
            canvas.itemconfig(mode_text, text=mode)

        if seconds_overall % 4 == 1:
            canvas.itemconfig(mode_text, text="")

        timer_r = window.after(1000, counting, seconds_overall + 1)


# --------------------------------- START/STOP ----------------------------------- #
def start_stop():
    global status
    global clock_running

    save_time()

    status = "work"

    clock_running = False
    initiation()


# ----------------------------------- MODE -------------------------------------- #
def change_mode():
    global mode
    global clock_running

    if mode == "now":
        mode = "day"

    elif mode == "day":
        mode = "now"

    clock_running = False
    initiation()


# ---------------------------- INITIATION MECHANISM ------------------------------ #
def initiation():
    global status
    global clock_running

    with open("time.csv", mode='r') as file:
        reader = csv.reader(file)
        data = []
        for row in reader:
            data.append(row[0])

    now = datetime.now()
    if not data or data[0][:10] != now.strftime("%Y-%m-%d"):
        save_day()

    # Wczytana data jako string
    data_string_last = data[-1]
    # Format daty w podanym stringu
    date_format = "%Y-%m-%d %H:%M:%S.%f"
    # Utwórz obiekt datetime z podanej daty
    parsed_date_last = datetime.strptime(data_string_last, date_format)

    if mode == "now":
        if len(data) % 2 != 0:
            #Czas który upłynął
            current_work_time = now - parsed_date_last
        else:
            status = "break"
            data_string_second_last = data[-2]
            parsed_date_second_last = datetime.strptime(data_string_second_last, date_format)
            current_work_time = parsed_date_last - parsed_date_second_last
    else:
        start_moment = []
        end_moment = []
        for i in range(len(data)):
            if i % 2 == 0:
                start_moment.append(datetime.strptime(data[i], date_format))
            else:
                end_moment.append(datetime.strptime(data[i], date_format))

        if len(data) % 2 != 0:
            end_moment.append(now)

        current_work_time = timedelta()
        for i in range(len(start_moment)):
            current_work_time += end_moment[i] - start_moment[i]

    godziny = int(current_work_time.total_seconds() // 60 // 60 % 60)
    if godziny < 10:
        godziny = f"0{godziny}"
    minuty = int(current_work_time.total_seconds() //60 % 60)
    if minuty < 10:
        minuty = f"0{minuty}"
    sekundy = int(current_work_time.total_seconds() % 60)
    if sekundy < 10:
        sekundy = f"0{sekundy}"

    canvas.itemconfig(timer_text, text=f"{godziny}:{minuty}")
    canvas.itemconfig(seconds_text, text=sekundy)
    seconds_overall = int(current_work_time.total_seconds())

    canvas.itemconfig(status_text, text=status)
    canvas.itemconfig(mode_text, text=mode)

    if len(data) % 2 != 0:
        clock_running = True
        counting(seconds_overall)




            # moment_startu = datetime.now()

            # with open("time.csv", mode='w', newline='') as file:
            #     writer = csv.writer(file)
            #     # writer.writerow(["Aktualna Godzina"])
            #     writer.writerow([moment_startu])







# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Study time")
window.config(padx=100, pady=50, bg=WHITE)

timer = Label(text="Timer", font=(FONT_NAME, 45), bg=WHITE, fg=DARK)
timer.grid(column=0, row=0)

instruction_1 = Label(text="Press left button to start and stop timer.", font=(FONT_NAME, 20), bg=WHITE, fg=DARK)
instruction_1.grid(column=0, row=1, pady=25)

instruction_2 = Label(text="Press right button to switch between current time and day time.",
                      font=(FONT_NAME, 20), bg=WHITE, fg=DARK)
instruction_2.grid(column=0, row=2)

canvas = Canvas(width=395, height=675, bg=WHITE, highlightthickness=0)
watch_img = PhotoImage(file="watch_img.png")
canvas.create_image(197, 337, image=watch_img)
timer_text = canvas.create_text(197, 308, text="00:00", fill=GREY, font=(FONT_NAME, 45, "bold"))
seconds_text = canvas.create_text(263, 350, text="00", fill=GREY, font=(FONT_NAME, 23, "bold"))
status_text = canvas.create_text(120, 200, text="work", fill=GREY, font=(FONT_NAME, 15, "bold"))
mode_text = canvas.create_text(265, 200, text="now", fill=GREY, font=(FONT_NAME, 15, "bold"))
canvas.grid(column=0, row=3, pady=25)

# Buttons
start_button = PhotoImage(file="button.png")
button_1 = Button(canvas, image=start_button, highlightthickness=0, command=start_stop)
button_1_window = canvas.create_window(120, 452, anchor=CENTER, window=button_1)

button_2 = Button(canvas, image=start_button, highlightthickness=0, command=change_mode)
button_2_window = canvas.create_window(265, 452, anchor=CENTER, window=button_2)

initiation()



window.mainloop()
