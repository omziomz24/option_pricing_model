from .utils import *

class Return_Volatility_Minimisation:
    def __init__(self, prices=None, log_returns=None, dt=1/252):
        """
        Initialize the minimisation object.
        
        Parameters:
        - prices: array-like, asset prices (if provided, log returns will be computed)
        - log_returns: array-like, log returns directly
        - dt: float, time step (default 1/252 for daily data)
        """
        self.dt = dt
        self.mu_est = None
        self.sigma_est = None
        self.prices = None
        self.log_returns = None
        self.historical_volatility = None  # Store historical volatility estimate
        
        if prices is not None:
            self.prices = np.array(prices)
            self.log_returns = np.diff(np.log(self.prices))
        elif log_returns is not None:
            self.log_returns = np.array(log_returns)

    def fetch_historical_volatility(self, ticker, stock_data, start, end, price_column='Adj Close'):
        self.dates = stock_data.index.to_list()
        self.prices = stock_data[price_column].squeeze().tolist()
        self.log_returns = np.diff(np.log(np.array(self.prices)))

        # Compute historical volatility estimate (Annualized)
        self.historical_volatility = np.std(self.log_returns) * np.sqrt(365)
        print(f"Fetched {len(self.prices)} prices for {ticker} from {start} to {end}.")
        print(f"Estimated Historical Volatility: {self.historical_volatility:.4f} ({self.historical_volatility*100:.2f}%)")

    def plot_historical_data(self, ticker: str):
        """
        Plot historical stock price data with dates on the x-axis.
        """
        if self.prices is None or not hasattr(self, "dates") or self.dates is None:
            raise ValueError("No price or date data available to plot. Please fetch historical data first.")
        
        plt.figure(figsize=(10, 5))
        plt.plot(self.dates, self.prices, label="Price")
        plt.title(f"Historical Stock Price Data {ticker}")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def get_valuation_price(self, valuation_date):
        """
        Get the stock price at the given valuation date.
        If an exact match is not found, return the most recent prior date's price.
        """
        # Convert valuation_date to pandas Timestamp for consistency
        valuation_date = pd.Timestamp(valuation_date)

        # Ensure self.dates is also pandas Timestamp objects
        self.dates = pd.to_datetime(self.dates)

        # Try to find an exact match
        for dt, price in zip(self.dates, self.prices):
            if dt == valuation_date:
                self.valuation_price = price
                return price

        # If no exact match, find the most recent prior date
        for dt, price in reversed(list(zip(self.dates, self.prices))):
            if dt < valuation_date:
                self.valuation_price = price
                return price

        # If still not found, return None
        return None


    @staticmethod
    def neg_log_likelihood(params, log_returns, dt, hist_vol):
        """
        Adjusted Negative log-likelihood function to avoid extreme volatility estimates.
        """
        mu, sigma = params
        if sigma <= 0 or sigma > hist_vol * 2:  # Constraint: Sigma should not be too large
            return np.inf
        
        N = len(log_returns)
        predicted_mean = (mu - 0.5 * sigma**2) * dt
        log_term = 0.5 * N * np.log(2 * np.pi * sigma**2 * dt)
        error_term = np.sum((log_returns - predicted_mean)**2) / (2 * sigma**2 * dt)
        return log_term + error_term

    def estimate_params(self, init_params=[0.05, 0.25]):
        """
        Estimate drift (mu) and volatility (sigma) by minimizing the adjusted negative log-likelihood.
        """
        if self.log_returns is None:
            raise ValueError("No log returns data available. Fetch historical data first.")
            
        bounds = [(-np.inf, np.inf), (1e-6, self.historical_volatility * 2)]
        result = minimize(
            self.neg_log_likelihood,
            init_params,
            args=(self.log_returns, self.dt, self.historical_volatility),
            bounds=bounds
        )
        
        if result.success:
            self.mu_est, self.sigma_est = result.x
        else:
            raise RuntimeError("Optimization failed.")

        # Blend MLE and historical volatility estimates to avoid overestimation
        self.sigma_est = (self.sigma_est + self.historical_volatility) / 2

        print(f"Mu Estimate: {self.mu_est:.4f}, Sigma Estimate: {self.sigma_est:.4f}")
        return self.mu_est, self.sigma_est
