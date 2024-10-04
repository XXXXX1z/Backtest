from tkinter import *

master = Tk()
master.title("Private Backtest Program")


Label(master, text="volatility").grid(row=0)
Label(master, text="Current Price").grid(row=1)
Label(master, text="Drift").grid(row=2)
Label(master, text="Time Increment").grid(row=3)
Label(master, text="Current Volume").grid(row=4)
Label(master, text="Average Volume").grid(row=5)
Label(master, text="Average True Range").grid(row=7)
Label(master, text="Random Noise").grid(row=8)

e1 = Entry(master)
e1.grid(row=0, column=1)
e2 = Entry(master)
e2.grid(row=1, column=1)
e3 = Entry(master)
e3.grid(row=2, column=1)
e4 = Entry(master)
e4.grid(row=3, column=1)
e5 = Entry(master)
e5.grid(row=4, column=1)
e6 = Entry(master)
e6.grid(row=5, column=1)
e8 = Entry(master)
e8.grid(row=7, column=1)
e9 = Entry(master)
e9.grid(row=8, column=1)


def submit_action():
    volatility = float(e1.get())
    Current_Price = float(e2.get())
    Drift = float(e3.get())
    Time_Increment = float(e4.get())
    Current_Volume = float(e5.get())
    Average_Volume = float(e6.get())
    ATR = float(e8.get())
    RandomNoise = float(e9.get())



submit_action()

mainloop()
