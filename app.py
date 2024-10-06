from tkinter import *
import tkinter as tk
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import numpy as np
import matplotlib.pyplot as plt

class App():
    def __init__(self, master):
        self.master = master
        self.volatility = None
        self.Current_Price = None
        self.Drift = None 
        self.Time_Increment = None 
        self.Current_Volume = None
        self.Average_Volume = None
        self.ATR = None
        self.RandomNoise = None

        self.base()
        
    def base(self):
        
        tk.Label(self.master, text="Volatility:").grid(row=0)
        self.e1 = tk.Entry(self.master)
        self.e1.grid(row=0, column=1)

        tk.Label(self.master, text="Current Price:").grid(row=1)
        self.e2 = tk.Entry(self.master)
        self.e2.grid(row=1, column=1)

        tk.Label(self.master, text="Drift:").grid(row=2)
        self.e3 = tk.Entry(self.master)
        self.e3.grid(row=2, column=1)

        tk.Label(self.master, text="Time Increment:").grid(row=3)
        self.e4 = tk.Entry(self.master)
        self.e4.grid(row=3, column=1)

        tk.Label(self.master, text="Current Volume:").grid(row=4)
        self.e5 = tk.Entry(self.master)
        self.e5.grid(row=4, column=1)

        tk.Label(self.master, text="Average Volume:").grid(row=5)
        self.e6 = tk.Entry(self.master)
        self.e6.grid(row=5, column=1)

        tk.Label(self.master, text="ATR:").grid(row=6)
        self.e8 = tk.Entry(self.master)
        self.e8.grid(row=6, column=1)

        tk.Label(self.master, text="Random Noise:").grid(row=7)
        self.e9 = tk.Entry(self.master)
        self.e9.grid(row=7, column=1)

        # Submit button
        self.submit_btn = tk.Button(self.master, text="Submit", command=self.equation)
        self.submit_btn.grid(row=8, columnspan=2)

        # Plot button
        self.plot_btn = tk.Button(self.master, text="Plot GBM", command=self.plot_gbm)
        self.plot_btn.grid(row=9, columnspan=2)

        # Result label
        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=10, columnspan=2)

    def equation(self):
        self.volatility = float(self.e1.get())
        self.Current_Price = float(self.e2.get().replace(",", "").replace("/", ""))
        self.Drift = float(self.e3.get().replace(",", "").replace("/", ""))
        self.Time_Increment = float(self.e4.get().replace(",", "").replace("/", ""))
        self.Current_Volume = float(self.e5.get().replace(",", "").replace("/", ""))
        self.Average_Volume = float(self.e6.get().replace(",", "").replace("/", ""))
        self.ATR = float(self.e8.get().replace(",", "").replace("/", ""))
        self.RandomNoise = float(self.e9.get().replace(",", "").replace("/", ""))
        
        vol_adjustment = self.volatility * (self.Current_Volume / self.Average_Volume)
        atr_adjustment = self.ATR / self.Current_Price
    
        dP_t = self.Current_Price * (self.Drift * self.Time_Increment + (vol_adjustment + atr_adjustment) * self.RandomNoise)
        new_price = self.Current_Price + dP_t
    
        self.result_label.config(text=f"New Price: {new_price:.2f}")
    
    def plot_gbm(self):
        if self.volatility is None or self.Time_Increment is None:
            return

       
        S0 = self.Current_Price  # Initial stock price
        mu = self.Drift  # Drift rate
        sigma = self.volatility  # Volatility
        T = 2  # Total time (1 year)
        dt = self.Time_Increment  # Time increment
        N = int(T / dt)  # Number of time steps
        M = 10  # Number of paths to simulate

        
        t = np.linspace(0, T, N)

        fig, ax = plt.subplots(figsize=(10, 6))
        for i in range(M):
            # Generate random noise
            W = np.random.normal(0, 1, N)  # Brownian increments
            # Simulate the GBM path
            S = S0 * np.exp(np.cumsum((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * W))
            plt.plot(t, S, label=f'Path {i + 1}')  # Label each path
        ax.set_title('Geometric Brownian Motion (GBM) Paths')
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
        
        ax.set_title('Geometric Brownian Motion (GBM) Paths')
        ax.set_xlabel('Time')
        ax.set_ylabel('Price')
    
        ax.legend(loc='upper left', bbox_to_anchor=(1, 1)) 
        
        plt.subplots_adjust(left=0.15, bottom=0.15, top=0.9)
        
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()

        canvas.get_tk_widget().grid(row=11, column=0, columnspan=2, padx=500, pady=20, sticky='nsew')

        
root = tk.Tk()
root.title("GBM Simulation")
root.geometry("1280x1020") 
app = App(root)
root.mainloop()