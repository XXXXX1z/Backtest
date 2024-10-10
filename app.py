from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import numpy as np
import matplotlib.pyplot as plt

#Here i setup a class becouse i want to acess a lot of variables inside other functions
class App():
    # we gonna define the default values of the params to 0 or None
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
        self.actual = None
        self.Forecast = None
        
        # Call the function
        self.base()
    #Here we setup the entire UI    
    def base(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=0)

        # Labels and Entry fields for parameters
        tk.Label(self.master, text="Volatility:").grid(row=0, column=0, padx=(20, 10), sticky='e') #define mainly the position
        self.e1 = tk.Entry(self.master)
        self.e1.grid(row=0, column=1, sticky='w') # define the row we want the label or button

        tk.Label(self.master, text="Current Price:").grid(row=1, column=0, padx=(20, 10), sticky='e')
        self.e2 = tk.Entry(self.master)
        self.e2.grid(row=1, column=1, sticky='w')

        tk.Label(self.master, text="Drift:").grid(row=2, column=0, padx=(20, 10), sticky='e')
        self.e3 = tk.Entry(self.master)
        self.e3.grid(row=2, column=1, sticky='w')

        tk.Label(self.master, text="Time Increment:").grid(row=3, column=0, padx=(20, 10), sticky='e')
        self.e4 = tk.Entry(self.master)
        self.e4.grid(row=3, column=1, sticky='w')

        tk.Label(self.master, text="Current Volume:").grid(row=4, column=0, padx=(20, 10), sticky='e')
        self.e5 = tk.Entry(self.master)
        self.e5.grid(row=4, column=1, sticky='w')

        tk.Label(self.master, text="Average Volume:").grid(row=5, column=0, padx=(20, 10), sticky='e')
        self.e6 = tk.Entry(self.master)
        self.e6.grid(row=5, column=1, sticky='w')

        tk.Label(self.master, text="ATR:").grid(row=6, column=0, padx=(20, 10), sticky='e')
        self.e8 = tk.Entry(self.master)
        self.e8.grid(row=6, column=1, sticky='w')

        tk.Label(self.master, text="Random Noise:").grid(row=7, column=0, padx=(20, 10), sticky='e')
        self.e9 = tk.Entry(self.master)
        self.e9.grid(row=7, column=1, sticky='w')
 
        self.submit_btn = tk.Button(self.master, text="Sumbit", command=self.CPI_params)#the comand servers for the button knows what it as to "Call"
        self.submit_btn.grid(row=8, column=1, padx=10, pady=30, sticky='w')
        
        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=9, column=0, columnspan=2, pady=10)

        self.forecast_frame = tk.Frame(self.master)
        self.forecast_frame.grid(row=10, column=0, columnspan=2, pady=20)
        
        #here we have the forecast and actual wich are where we gonna put the values

        tk.Label(self.forecast_frame, text="Forecast:").grid(row=0, column=0, padx=(20, 10), sticky='e')
        self.forecast_entry = tk.Entry(self.forecast_frame)
        self.forecast_entry.grid(row=0, column=1, sticky='w')

        tk.Label(self.forecast_frame, text="Actual:").grid(row=1, column=0, padx=(20, 10), sticky='e')
        self.actual_entry = tk.Entry(self.forecast_frame)
        self.actual_entry.grid(row=1, column=1, sticky='w')
        
        self.cpi_var = tk.IntVar()
        self.nfp_var = tk.IntVar()

    # Add CPI and NFP checkboxes below Forecast and Actual entries
        self.cpi_checkbox = tk.Checkbutton(self.forecast_frame, text="CPI", variable=self.cpi_var, command=self.CPI_params)
        self.cpi_checkbox.grid(row=2, column=0, padx=(1780, 10), pady=10, sticky='w')

        self.nfp_checkbox = tk.Checkbutton(self.forecast_frame, text="NFP", variable=self.nfp_var)
        self.nfp_checkbox.grid(row=2, column=1, padx=(10, 10), pady=10, sticky='w')
        
        self.plot_frame = tk.Frame(self.master)
        self.plot_frame.grid(row=11, column=0, columnspan=2, pady=20)
    
    #here we will set the params of when we set CPI check box & the actual is greater than forecast
    def CPI_params(self):
        forecast_value = self.forecast_entry.get()
        actual_value = self.actual_entry.get()
        
        if not forecast_value or not actual_value:
           messagebox.showerror("Input Error", "Please enter values for both Forecast and Actual.")
           return

        try:
        # Convert the values to float and store them in self.Forecast and self.actual
           self.Forecast = float(forecast_value)
           self.actual = float(actual_value)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
            return
        
        if self.cpi_var.get():
            if self.actual > self.Forecast:
                S0 = 100  # Initial stock price
                mu = 0.02   # Drift rate
                sigma = 0.25  # Volatility
                T = 2  # Total time (2 years)
                dt = 0.003968  # Time increment
                N = int(T / dt)  # Number of time steps
                M = 1  # Number of paths to simulate

                t = np.linspace(0, T, N)

                for widget in self.plot_frame.winfo_children():
                    widget.destroy()

                fig = Figure(figsize=(10, 5), dpi=100)
                plot1 = fig.add_subplot(111)

                for i in range(M):
                    W = np.random.normal(0, 1, N)  # Brownian increments
                    S = S0 * np.exp(np.cumsum((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * W))
                    plot1.plot(t, S, label=f'Path {i + 1}')  # Label each path

                plot1.set_title('Simulated Stock Price Paths')
                plot1.set_xlabel('Time (Years)')
                plot1.set_ylabel('Stock Price')
                plot1.legend()

                canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
                canvas.draw()
                canvas.get_tk_widget().pack()
        
    
    def plot_simulation(self):
        if self.volatility is None or self.Time_Increment is None: #if the volatility and Time Increment have values on it, return this:
            return

        S0 = self.Current_Price  # Initial stock price
        mu = self.Drift  # Drift rate
        sigma = self.volatility  # Volatility
        T = 2  # Total time (2 years)
        dt = self.Time_Increment  # Time increment
        N = int(T / dt)  # Number of time steps
        M = 10  # Number of paths to simulate

        t = np.linspace(0, T, N)

        # Create a new window for the plot
        window = Toplevel(self.master)
        window.title("Simulated Stock Price Paths")

        fig = Figure(figsize=(5, 5), dpi=100)#Size of the plot
        plot1 = fig.add_subplot(111)

        for i in range(M):#So here is for iliterate in the range of what we set up on M
            W = np.random.normal(0, 1, N)  # Brownian increments
            S = S0 * np.exp(np.cumsum((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * W))
            plot1.plot(t, S, label=f'Path {i + 1}')  # Label each path

        plot1.set_title('Simulated Stock Price Paths')
        plot1.set_xlabel('Time (Years)')
        plot1.set_ylabel('Stock Price')
        plot1.legend()


        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__=='__main__': #the mains function to call 
   root = tk.Tk()
   root.title("GBM Simulation")
   root.geometry("1920x1080") 
   app = App(root)
   root.mainloop()