from .utils import *
from .option_strike import Strike
from .stochastic_process import Stochastic_Process

class European_Option_Simulation:
    
    # tte = Time to Expiration
    # rfr = Risk Free Rate
    def __init__(self, stochastic_process_type: str, strike: Strike, sims: int, initial_price: float, drift: float, \
                 delta_t: float, volatility: float, tte: float, rfr_appropriate_dates):
        self.stochastic_process_type = stochastic_process_type
        self.strike = strike
        self.sims = sims
        self.initial_price = initial_price
        self.drift = drift
        self.delta_t = delta_t
        self.volatility = volatility
        self.tte = tte
        self.rfr_range = rfr_appropriate_dates

    def run_simulation_batch(self, batch_size: int):
        simulations = []
        for _ in range(batch_size):
            stochastic_process = Stochastic_Process(self.stochastic_process_type, self.initial_price, self.drift, self.delta_t, self.volatility)
            tte_initial = self.tte

            # while option has not expired move and decrement to next time step
            while (tte_initial - stochastic_process.delta_t) > 0:
                tte_initial -= stochastic_process.delta_t
                stochastic_process.time_step()

            simulations.append(stochastic_process.prices)
        
        return simulations
    

    def run_multiprocessing(self, processes: int):
        batch_size = self.sims // processes
        batches = [batch_size] * processes

        with Pool(processes=processes) as pool:
            results = pool.map(self.run_simulation_batch, batches)

        all_simulations = [sim for sublist in results for sim in sublist]

        # Compute Call & Put Payoffs
        # Following print is for DEBUGGING
        # print([result[-1] for result in all_simulations][:30])
        payoffs_call = [max(sim[-1] - self.strike.Strike, 0) for sim in all_simulations]  # Call: max(S_T - K, 0)
        payoffs_put = [max(self.strike.Strike - sim[-1], 0) for sim in all_simulations]  # Put: max(K - S_T, 0)

        # Compute present value of both option prices
        discount_factor = math.exp(-self.tte * np.average(self.rfr_range['Rate']))
        call_price = np.average(payoffs_call) * discount_factor
        put_price = np.average(payoffs_put) * discount_factor

        return call_price, put_price, all_simulations

    def plot_option_payoffs(self):
        """
        Plots the payoff of a European Call and Put option at expiration
        for a range of different spot prices (S_T).
        """
        # Generate a range of spot prices from 0 to 2x the strike price
        spot_prices = np.linspace(0, 2 * self.strike.Strike, 100)

        # Calculate Call and Put Payoffs
        call_values = np.maximum(spot_prices - self.strike.Strike, 0)  # Call: max(S_T - K, 0)
        put_values = np.maximum(self.strike.Strike - spot_prices, 0)   # Put: max(K - S_T, 0)

        # Plot Call and Put Values
        plt.figure(figsize=(10, 6))
        plt.plot(spot_prices, call_values, label="Call Option", color='blue', linewidth=2)
        plt.plot(spot_prices, put_values, label="Put Option", color='red', linewidth=2)

        # Labels & Styling
        plt.axhline(0, color='black', linewidth=1, linestyle='--')
        plt.axvline(self.strike.Strike, color='black', linewidth=1, linestyle='--', label="Strike Price")
        plt.xlabel("Spot Price (S_T)")
        plt.ylabel("Option Value")
        plt.title("European Call & Put Option Payoff at Expiration")
        plt.legend()
        plt.grid(True)

        plt.show()

    def plot_simulations(self, all_simulations: list):
        plt.figure(figsize=(10,6))

        for path in all_simulations:
            rand_col = np.random.rand(3,)
            plt.plot(path, color=rand_col, alpha=0.5)
        
        # Average price path in thick red line
        avg_path = np.mean(all_simulations, axis=0)
        plt.plot(avg_path, color='red', label='Average Path', linewidth=2)

        plt.title(f'Simulated Price Paths for {self.stochastic_process_type}')
        plt.xlabel('Time Steps')
        plt.ylabel('Price')
        plt.grid(True)
        plt.show()