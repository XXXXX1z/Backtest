from tkinter import *
import tkinter as tk
from tkinter import messagebox
import numpy as np
import mplfinance as mpf
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class App():
    def __init__(self, master):
        self.master = master
        self.volatility = None
        self.Current_Price = None
        self.Drift = None 
        self.Time_Increment = None 
        self.actual = None
        self.Forecast = None
        self.base()

    def base(self):
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=0)

        tk.Label(self.master, text="Volatility:").grid(row=0, column=0, padx=(20, 10), sticky='e')
        self.e1 = tk.Entry(self.master)
        self.e1.grid(row=0, column=1, sticky='w')

        tk.Label(self.master, text="Current Price:").grid(row=1, column=0, padx=(20, 10), sticky='e')
        self.e2 = tk.Entry(self.master)
        self.e2.grid(row=1, column=1, sticky='w')

        tk.Label(self.master, text="Drift:").grid(row=2, column=0, padx=(20, 10), sticky='e')
        self.e3 = tk.Entry(self.master)
        self.e3.grid(row=2, column=1, sticky='w')

        tk.Label(self.master, text="Time Increment:").grid(row=3, column=0, padx=(20, 10), sticky='e')
        self.e4 = tk.Entry(self.master)
        self.e4.grid(row=3, column=1, sticky='w')

        self.submit_btn = tk.Button(self.master, text="Submit", command=self.CPI_params)
        self.submit_btn.grid(row=8, column=1, padx=10, pady=30, sticky='w')
        
        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=9, column=0, columnspan=2, pady=10)

        self.forecast_frame = tk.Frame(self.master)
        self.forecast_frame.grid(row=10, column=0, columnspan=2, pady=20)

        tk.Label(self.forecast_frame, text="Forecast:").grid(row=0, column=0, padx=(20, 10), sticky='e')
        self.forecast_entry = tk.Entry(self.forecast_frame)
        self.forecast_entry.grid(row=0, column=1, sticky='w')

        tk.Label(self.forecast_frame, text="Actual:").grid(row=1, column=0, padx=(20, 10), sticky='e')
        self.actual_entry = tk.Entry(self.forecast_frame)
        self.actual_entry.grid(row=1, column=1, sticky='w')

        self.cpi_var = tk.IntVar()
        self.nfp_var = tk.IntVar()

        self.cpi_checkbox = tk.Checkbutton(self.forecast_frame, text="CPI", variable=self.cpi_var, command=self.CPI_params)
        self.cpi_checkbox.grid(row=2, column=0, padx=(1780, 10), pady=10, sticky='w')

        self.nfp_checkbox = tk.Checkbutton(self.forecast_frame, text="NFP", variable=self.nfp_var)
        self.nfp_checkbox.grid(row=2, column=1, padx=(10, 10), pady=10, sticky='w')
        
        self.plot_frame = tk.Frame(self.master)
        self.plot_frame.grid(row=11, column=0, columnspan=2, pady=20)

    def CPI_params(self):
        forecast_value = self.forecast_entry.get()
        actual_value = self.actual_entry.get()
        
        if not forecast_value or not actual_value:
            messagebox.showerror("Input Error", "Please enter values for both Forecast and Actual.")
            return

        try:
            self.Forecast = float(forecast_value)
            self.actual = float(actual_value)
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numeric values.")
            return
        
        if self.cpi_var.get():
            if self.actual > self.Forecast:
                self.simulate_prices(mu=0.02)  # Simulate price path with positive drift
            elif self.actual < self.Forecast:
                self.simulate_prices(mu=-0.02)  # Simulate price path with negative drift

    def simulate_prices(self, mu):
        S0 = 100  # Initial stock price
        sigma = 0.25  # Volatility
        T = 180  # Total time
        dt = 1  # Time increment
        N = int(T / dt)  # Number of time steps

        self.e1.delete(0, tk.END)
        self.e1.insert(0, sigma)  # Volatility

        self.e2.delete(0, tk.END)
        self.e2.insert(0, 100)  # Current Price

        self.e3.delete(0, tk.END)
        self.e3.insert(0, mu)  # Drift

        self.e4.delete(0, tk.END)
        self.e4.insert(0, dt)

        # Clear previous plots
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        price_data = []

        # Simulate one path
        W = np.random.normal(0, 1, N)  # Brownian increments
        S = S0 * np.exp(np.cumsum((mu - 0.5 * sigma**2) * dt + (sigma * np.sqrt(dt) * W)))

        # Generate OHLC data for candlestick chart
        for i in range(1, len(S)):
            # Define Open, High, Low, Close for each time step
            open_price = S[i-1]
            close_price = S[i]
            high_price = max(open_price, close_price)
            low_price = min(open_price, close_price)
            price_data.append([pd.Timestamp.now() + pd.Timedelta(days=i), open_price, high_price, low_price, close_price])  # [Time, Open, High, Low, Close]

        # Create a DataFrame for mplfinance
        df = pd.DataFrame(price_data, columns=['Time', 'Open', 'High', 'Low', 'Close'])
        df.set_index('Time', inplace=True)

        # Define custom colors
        mc = mpf.make_marketcolors(up='green', down='red', edge='black', wick='black', inherit=True)  # Set bodies green/red and wicks black
        s = mpf.make_mpf_style(marketcolors=mc)

        # Plotting candlestick chart using mplfinance
        fig, ax = mpf.plot(df, type='candle', style=s, volume=False, show_nontrading=False, returnfig=True)

        # Create a FigureCanvasTkAgg widget for embedding
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

if __name__=='__main__':
    root = tk.Tk()
    root.title("GBM Simulation")
    root.geometry("1920x1080") 
    app = App(root)
    root.mainloop()
