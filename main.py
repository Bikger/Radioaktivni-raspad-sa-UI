from selenium import webdriver
from tkinter import *
import numpy as np
import math
import pyautogui
import re
from time import sleep

e = 2.71828

window = Tk()
half_life = StringVar()
time = StringVar()
I0 = StringVar()
m0 = StringVar()
m = StringVar()
half_life_2 = StringVar()


def GUI():

    # Half time
    half_life_label = Label(window, text="Vrijeme poluraspada (h)", fg='Black', font=("Helvetica", 17))
    half_life_label.place(x=20, y=80)
    half_life_entry = Entry(window, textvariable=half_life)
    half_life_entry.place(x=280, y=80)
    half_life_entry.focus()

    # Top label
    lbl1 = Label(window, text="Unesite parametre: ", fg='Black', font=("Helvetica", 24, "bold"))
    lbl1.place(x=20, y=30)

    # Time
    time_label = Label(window, text="Vrijeme izloženo radijaciji (min)", font=("Helvetica", 17))
    time_label.place(x=20, y=120)
    time_entry = Entry(window, textvariable=time)
    time_entry.place(x=280, y=120)

    # Starting amount of radiation
    I0_label = Label(window, text="Početna količina radijacije (mSv)", font=("Helvetica", 17))
    I0_label.place(x=20, y=160)
    I0_entry = Entry(window, textvariable=I0)
    I0_entry.place(x=280, y=160)

    # Submit button
    Submit = Button(text="Izračunaj", fg="Black",  command=submit_clicked, width=50, height=2)
    Submit.place(x=20, y=200)

    window.title("Radioaktivni raspad")
    window.geometry("500x650+650+200")
    window.mainloop()

def submit_clicked():
    # Get variables from input
    x = half_life.get()
    y = time.get()
    z = I0.get()

    # calculate
    if "," in x:
        x = x.replace(",", ".")
    if bool(re.search("d.", x)) == True:
        x = x.strip().split()
        x = x[0]
        x = float(x) * 24

    if "," in y:
        y = y.replace(",", ".")
    if "," in z:
        z = z.strip().split()
        z = z[0]
        z = float(z.replace(",", "."))
    else:
        z = z.strip().split()
        z = z[0]
        z = float(z)

    if "h" in y:
        y = y.strip().split()
        y = y[0]
        y = float(y) * 60

    if bool(re.search("s.", str(y))) == True:
        y = y.strip().split()
        y = y[0]
        y = float(y) / 60
    else:
        y = float(y) / 60

    lam = np.log(2) / float(x)
    X = z * math.exp(-lam * y)
    x2 = X + z

    # Result
    Res = Label(window, text="Ukupna količina radijacije iznosi {} mSv. ".format(x2), font=("Helvetica", 17, "bold"))
    Res.place(x=20, y=250)
    Res_box = LabelFrame(bg="Black", bd=5)
    Res_box.place(x=20, y=250)

    # m0 input
    m0_label = Label(window, text="Unesite početnu količinu radiofarmaka (g): ", font=("Helvetica", 17))
    m0_label.place(x=20, y=290)
    m0_entry = Entry(window, textvariable=m0)
    m0_entry.place(x=20, y=320)

    # m input
    m_label = Label(window, text="Unesite masu radiofarmaka koja ostaje u organizmu (g): ", font=("Helvetica", 17))
    m_label.place(x=20, y=370)
    m_entry = Entry(window, textvariable=m)
    m_entry.place(x=20, y=400)

    # half_life_2 input
    half_life_2_label = Label(window, text="Unesite vrijeme poluraspada (h): ", font=("Helvetica", 17))
    half_life_2_label.place(x=20, y=450)
    half_life_2_entry = Entry(window, textvariable=half_life_2)
    half_life_2_entry.place(x=20, y=480)

    #Submit2 button
    submit2 = Button(text="Koliko dugo pacijent treba ostati u bolnici?", width=50, height=2, command=callback)
    submit2.place(x=20, y=520)

def callback():
    x = m0.get()
    y = m.get()
    z = half_life_2.get()

    if "," in x:
        x = x.replace(",", ".")
    if "," in y:
        y = y.replace(",", ".")
    if "," in z:
        z = z.replace(",", ".")

    if bool(re.search("d.", z)) == True:
        z = z.strip().split()
        z = z[0]
        z = float(z) * 24
    z = float(z)

    if "kg" in x:
        x = x.strip().split()
        x = x[0]
        x = float(x) * 1000
    if "kg" in y:
        y = y.strip().split()
        y = y[0]
        y = float(y) * 1000

    M = float(y) / float(x)
    ftime = -z * math.log10(M) / math.log10(2)

    # Result 2
    Res_2 = Label(window, text="Pacijent treba ostati u bolnici još {} sati. ".format(ftime), font=("Helvetica", 17, "bold"))
    Res_2.place(x=20, y=570)

    #Graph button
    Graph = Button(window, text="Graph", width=10, height=2, command=botPlot)
    Graph.place(x=390, y=590)


def botPlot():
    driver = webdriver.Firefox()
    driver.get("https://www.geogebra.org/calculator")
    sleep(5)

    pyautogui.click(250, 200)
    pyautogui.write("y")
    pyautogui.click(850, 700)
    pyautogui.write("I0 + e")
    pyautogui.moveRel(-400, - 50)
    pyautogui.click()
    pyautogui.write("/ln2-T")
    for i in range(2):
        pyautogui.press("right")
    pyautogui.write("+x")
    pyautogui.press("enter")
    sleep(7)

    driver.quit()

GUI()
