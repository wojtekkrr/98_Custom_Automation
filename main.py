from tkinter import *
from datetime import datetime
import math
import csv

# ---------------------------- CONSTANTS ------------------------------- #
WHITE = "#f8f8f8"
GREY = "#EEEEEE"
DARK = "#393E46"
DARK_GREY = "#929AAB"

FONT_NAME = "Courier"

# ---------------------------- VARIABLES ------------------------------- #
status = "off"

mode = "now"

# ---------------------------------- SAVE DAY ------------------------------------ #
def save_day():
    now = datetime.now()
    with open("time.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([now])

# ----------------------------- COUNTING MECHANISM ------------------------------- #
def counting():
    global status

    with open("time.csv", mode='r') as file:
        reader = csv.reader(file)
        data = []
        for row in reader:
            data.append(row[0])

    now = datetime.now()
    if not data or data[0][:10] != now.strftime("%Y-%m-%d"):
        save_day()
    elif data[0][:10] == now.strftime("%Y-%m-%d"):
        if len(data) % 2 != 0:
            #Wczytana data jako string
            data_string = data[-1]
            # Format daty w podanym stringu
            date_format = "%Y-%m-%d %H:%M:%S.%f"
            # Utwórz obiekt datetime z podanej daty
            parsed_date = datetime.strptime(data_string, date_format)
            #Czas który upłynął
            current_work_time = now - parsed_date
            minuty = int(current_work_time.total_seconds() // 60 % 60)
            if minuty < 10:
                minuty = f"0{minuty}"
            sekundy = int(current_work_time.total_seconds() % 60)
            if sekundy < 10:
                sekundy = f"0{sekundy}"
            canvas.itemconfig(timer_text, text=f"{minuty}:{sekundy}")
        else:
            pass



            # moment_startu = datetime.now()

            # with open("time.csv", mode='w', newline='') as file:
            #     writer = csv.writer(file)
            #     # writer.writerow(["Aktualna Godzina"])
            #     writer.writerow([moment_startu])





    # count_min = math.floor(count / 60)
    # count_sec = count % 60
    # if count_sec < 10:
    #     count_sec = f'0{count_sec}'
    # if count_min < 10:
    #     count_min = f'0{count_min}'
    # canvas.itemconfig(timer_text, text=f'{count_min}:{count_sec}')
    # if count > 0:
    #     global timer_r
    #     timer_r = window.after(1000, counting)
    # else:
    #     start_timer()
    #     text = ""
    #     work_sessions = math.floor(reps/2)
    #     for _ in range(work_sessions):
    #         text += "✔"
    #     check_mark.config(text=text)

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
status_text = canvas.create_text(120, 200, text="work", fill=GREY, font=(FONT_NAME, 15, "bold"))
mode_text = canvas.create_text(265, 200, text="now", fill=GREY, font=(FONT_NAME, 15, "bold"))
canvas.grid(column=0, row=3, pady=25)

# Buttons
start_button = PhotoImage(file="button.png")
button_1 = Button(canvas, image=start_button, highlightthickness=0)
button_1_window = canvas.create_window(120, 452, anchor=CENTER, window=button_1)

button_2 = Button(canvas, image=start_button, highlightthickness=0)
button_2_window = canvas.create_window(265, 452, anchor=CENTER, window=button_2)

counting()



window.mainloop()
