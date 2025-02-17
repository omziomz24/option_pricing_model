from .utils import *
import matplotlib.dates as mdates

class Multi_Plot_Navigator:
    """
    Class to display multiple plots in one interactive Matplotlib figure
    using arrow buttons to navigate between different graphs.
    """
    def __init__(self, simulation, minimiser, ticker, all_simulations, call_price, put_price, spot_price_0):
        self.simulation = simulation
        self.minimiser = minimiser
        self.ticker = ticker
        self.all_simulations = all_simulations
        self.call_price = call_price
        self.put_price = put_price
        self.spot_price = spot_price_0

        # Adjust graphing window size
        self.fig, self.ax = plt.subplots(figsize=(10, 6))  
        self.index = 0  # Track which plot is displayed
        self.plots = [self.plot_option_payoffs, self.plot_historical_data, self.plot_simulations]  # All plots

        # Connect navigation to key press events
        self.fig.canvas.mpl_connect('key_press_event', self.on_key)
        self.update_plot()  # Show the first plot
        plt.show()

    def update_plot(self):
        """Clears the figure and plots the current graph based on index."""
        self.ax.clear()
        # Remove any previous hover annotations if they exist
        if hasattr(self, 'annot'):
            self.annot.set_visible(False)
        if hasattr(self, 'annot_hist'):
            self.annot_hist.set_visible(False)
        self.plots[self.index]()  # Call the appropriate plotting function
        self.fig.canvas.draw()  # Refresh the figure

    def on_key(self, event):
        """Handles left/right arrow key presses to switch plots."""
        if event.key == "right":
            self.index = (self.index + 1) % len(self.plots)  # Cycle forward
        elif event.key == "left":
            self.index = (self.index - 1) % len(self.plots)  # Cycle backward
        self.update_plot()

    def plot_option_payoffs(self):
        """Plots the payoff diagram for Call and Put options with interactive hover and markers for actual model prices."""
        spot_prices = np.linspace(0, 2 * self.simulation.strike.Strike, 100)
        call_values = np.maximum(spot_prices - self.simulation.strike.Strike, 0)  # Call: max(S_T - K, 0)
        put_values = np.maximum(self.simulation.strike.Strike - spot_prices, 0)   # Put: max(K - S_T, 0)

        # Plot Call & Put Option Payoffs
        call_line, = self.ax.plot(spot_prices, call_values, label="Call Option", color='blue', linewidth=2)
        put_line, = self.ax.plot(spot_prices, put_values, label="Put Option", color='red', linewidth=2)
        
        # Add vertical dotted line at spot price & legend update
        self.ax.axvline(self.spot_price, color='black', linewidth=1, linestyle='--', label=f"Spot Price: ${self.spot_price:.2f}")
        self.ax.set_title("European Call & Put Option Payoff at Expiration", fontsize=14)
        self.ax.set_xlabel("Spot Price", fontsize=12)
        self.ax.set_ylabel("Option Value", fontsize=12)
        self.ax.legend(loc="upper right", fontsize=12, frameon=True, fancybox=True, edgecolor="black")
        self.ax.grid(True)

        # Plot markers for model-predicted Call & Put prices
        actual_call_x = self.spot_price  
        actual_call_y = self.call_price  
        actual_put_x = self.spot_price  
        actual_put_y = self.put_price  

        self.ax.scatter(actual_call_x, actual_call_y, color='blue', s=100, zorder=3)
        self.ax.scatter(actual_put_x, actual_put_y, color='red', s=100, zorder=3)

        # Add annotations with arrows
        self.ax.annotate(f"Call: ${actual_call_y:.2f}", xy=(actual_call_x, actual_call_y), 
                         xytext=(actual_call_x + 5, actual_call_y + 5),
                         arrowprops=dict(facecolor='blue', arrowstyle="->"), fontsize=12, 
                         bbox=dict(facecolor="white", edgecolor="blue", boxstyle="round,pad=0.3"))
        self.ax.annotate(f"Put: ${actual_put_y:.2f}", xy=(actual_put_x, actual_put_y), 
                         xytext=(actual_put_x - 15, actual_put_y + 5),
                         arrowprops=dict(facecolor='red', arrowstyle="->"), fontsize=12, 
                         bbox=dict(facecolor="white", edgecolor="red", boxstyle="round,pad=0.3"))

        # Create annotation for hover on option payoffs
        self.annot = self.ax.annotate("", xy=(0, 0), xytext=(15, 15),
                                      textcoords="offset points",
                                      bbox=dict(boxstyle="round,pad=0.3", fc="yellow", ec="black", lw=1),
                                      arrowprops=dict(arrowstyle="->", color="black"))
        self.annot.set_visible(False)

        # Bind mouse hover event for option payoffs
        self.fig.canvas.mpl_connect("motion_notify_event", 
                                    lambda event: self.hover(event, spot_prices, call_values, put_values))

    def hover(self, event, spot_prices, call_values, put_values):
        """Handles hover event to display Call & Put option values dynamically."""
        if event.inaxes == self.ax:
            x = event.xdata  
            if x is not None:
                index = np.argmin(np.abs(spot_prices - x))
                call_y = call_values[index]
                put_y = put_values[index]

                # Determine which curve the cursor is nearer to
                if np.abs(event.ydata - call_y) < np.abs(event.ydata - put_y):
                    y = call_y
                    text = f"Call: ${y:.2f}"
                else:
                    y = put_y
                    text = f"Put: ${y:.2f}"

                self.annot.xy = (x, y)
                self.annot.set_text(text)
                self.annot.set_visible(True)
                self.fig.canvas.draw_idle()
            else:
                self.annot.set_visible(False)
        else:
            self.annot.set_visible(False)

    def plot_simulations(self):
        """Plots the simulated stock price paths."""
        for path in self.all_simulations:
            rand_col = np.random.rand(3,)
            self.ax.plot(path, color=rand_col, alpha=0.5)
        
        avg_path = np.mean(self.all_simulations, axis=0)
        self.ax.plot(avg_path, color='red', label='Average Path', linewidth=2)

        self.ax.set_title(f'Simulated Price Paths for {self.simulation.stochastic_process_type}', fontsize=14)
        self.ax.set_xlabel('Time Steps', fontsize=12)
        self.ax.set_ylabel('Price', fontsize=12)
        self.ax.legend()
        self.ax.grid(True)

    def plot_historical_data(self):
        """Plots historical stock price data with interactive hover displaying the asset's price."""
        if self.minimiser.prices is not None and hasattr(self.minimiser, "dates"):
            self.ax.plot(self.minimiser.dates, self.minimiser.prices, label="Price")
            self.ax.set_title(f"Historical Stock Price Data {self.ticker}", fontsize=14)
            self.ax.set_xlabel("Date", fontsize=12)
            self.ax.set_ylabel("Price", fontsize=12)
            self.ax.legend()
            self.ax.grid(True)
            
            # Create annotation for historical data hover
            self.annot_hist = self.ax.annotate("", xy=(0,0), xytext=(15,15),
                                                 textcoords="offset points",
                                                 bbox=dict(boxstyle="round", fc="w"),
                                                 arrowprops=dict(arrowstyle="->"))
            self.annot_hist.set_visible(False)
            
            # Convert dates to numerical format for comparison with event.xdata
            self.dates_num = mdates.date2num(self.minimiser.dates)
            
            # Connect hover event for historical data
            self.fig.canvas.mpl_connect("motion_notify_event", self.hover_historical)
        else:
            self.ax.text(0.5, 0.5, "No Historical Data Available", fontsize=12, ha='center')
    
    def hover_historical(self, event):
        """Handles hover event for the historical data plot to display the asset's price."""
        if event.inaxes == self.ax:
            # Ensure that the historical data exists
            if not hasattr(self, 'dates_num'):
                return
            
            if event.xdata is None or event.ydata is None:
                self.annot_hist.set_visible(False)
                self.fig.canvas.draw_idle()
                return

            # Find the index of the closest date
            index = np.argmin(np.abs(self.dates_num - event.xdata))
            # Get the corresponding date and price
            x_val = self.minimiser.dates[index]
            y_val = self.minimiser.prices[index]
            
            # Update annotation position and text
            self.annot_hist.xy = (mdates.date2num(x_val), y_val)
            self.annot_hist.set_text(f"Price: ${y_val:.2f}")
            self.annot_hist.set_visible(True)
            self.fig.canvas.draw_idle()
        else:
            if hasattr(self, 'annot_hist'):
                self.annot_hist.set_visible(False)
                self.fig.canvas.draw_idle()


    # try:
    #     # Plot the simulations
    #     plot = str(input(f"\n\033[1mPlot simulations and stock price (Y/N):\033[0m ")).upper()
    #     if plot == "Y":
    #         Multi_Plot_Navigator(simulation=simulation,
    #                         minimiser=minimiser,
    #                         ticker=ticker,
    #                         all_simulations=all_simulations,
    #                         call_price=call_price,
    #                         put_price=put_price,
    #                         spot_price_0=spot_price)
    # except KeyboardInterrupt:
    #     print("\n\nScript interrupted by user. Exiting gracefully...\n")
    #     exit(0)  # Exits the script without error
    