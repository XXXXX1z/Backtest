from tkinter import *

master = Tk()
master.title("Private Backtest Program")


Label(master, text="volatility").grid(row=0)  # Volatility (σ): Measures the rate of price fluctuations (percentage) over time.
Label(master, text="Current Price").grid(row=1) #The current price of the asset being evaluated.
Label(master, text="Drift").grid(row=2) #The expected return or trend in the price movement over time (a small value representing expected upward/downward
Label(master, text="Time Increment").grid(row=3) #Time Increment (dt): The time step for each price movement (e.g., 1/252 for daily trading steps).
Label(master, text="Current Volume").grid(row=4) #Current Volume (Volume_t): The current number of shares or contracts traded.
Label(master, text="Average Volume").grid(row=5) #Average Volume: The average volume traded over a given historical period.
Label(master, text="Average True Range").grid(row=7) #Average True Range (ATR): A technical indicator representing the average price range of the asset over a specific period.
Label(master, text="Random Noise").grid(row=8) # Random Noise (dW_t): A random value from a normal distribution to simulate unpredictable price changes (often related to volatility).

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
    volatility = float(e1.get()) #here what we are doing is basicly creating variables, and inside them we are saying for them to "get" the input box from abox
    Current_Price = float(e2.get())
    Drift = float(e3.get())
    Time_Increment = float(e4.get())
    Current_Volume = float(e5.get())
    Average_Volume = float(e6.get())
    ATR = float(e8.get())
    RandomNoise = float(e9.get())
    
    vol_adjustment = volatility * (Current_Volume / Average_Volume)
    atr_adjustment = ATR / Current_Price
    
    dP_t = Current_Price * (Drift * Time_Increment + (vol_adjustment + atr_adjustment) * RandomNoise) #simple represation of equation
    new_price = Current_Price + dP_t
    
    result_label.config(text=f"New Price: {new_price:.2f}")

submit_button = Button(master, text="Submit", command=submit_action)
submit_button.grid(row=8, column=2)

result_label = Label(master, text="New Price: ")
result_label.grid(row=9, column=1)

master.mainloop()

