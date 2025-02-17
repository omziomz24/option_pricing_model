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

    def fetch_historical_data(self, ticker, start, end, price_column='Adj Close'):
        """
        Retrieve historical stock price data using yfinance.
        """
        data = yf.download(ticker, start=start, end=end)
        if data.empty:
            raise ValueError(f"No data found for ticker: {ticker}")
        
        if price_column not in data.columns:
            if 'Close' in data.columns:
                price_column = 'Close'
            else:
                raise ValueError(f"Neither '{price_column}' nor 'Close' found in data.")
        
        self.dates = data.index.to_list()
        self.prices = data[price_column].squeeze().tolist()
        self.log_returns = np.diff(np.log(np.array(self.prices)))

        print(f"Fetched {len(self.prices)} prices for {ticker} from {start} to {end}.")

    def plot_historical_data(self):
        """
        Plot historical stock price data with dates on the x-axis.
        """
        if self.prices is None or not hasattr(self, "dates") or self.dates is None:
            raise ValueError("No price or date data available to plot. Please fetch historical data first.")
        
        plt.figure(figsize=(10, 5))
        plt.plot(self.dates, self.prices, label="Price")
        plt.title("Historical Stock Price Data")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

    def get_valuation_price(self, valuation_date):
        """
        Get the stock price at the nearest available date to the given valuation date.
        If an exact match is not found, return the next available future price.
        """
        # Convert valuation_date to pandas Timestamp for consistency
        valuation_date = pd.Timestamp(valuation_date)

        # Ensure self.dates is a **normal list** of Timestamps
        self.dates.sort()  # Ensure it's sorted in ascending order

        # If no data is available, return None
        if len(self.dates) == 0:
            print("🚨 ERROR: No historical dates found!")
            return None

        # If requested date is before the first available date, print warning
        if valuation_date < self.dates[0]:
            print(f"⚠️ Requested date {valuation_date} is before the first available date {self.dates[0]}.")

        # Check if an exact match exists
        for dt, price in zip(self.dates, self.prices):
            if dt == valuation_date:
                print(f"✅ Exact match found: {dt} → Price: {price}")
                self.valuation_price = price
                return price

        # Find the **smallest** available future date
        for dt, price in zip(self.dates, self.prices):
            if dt > valuation_date:
                print(f"✅ Rounded up to next available date: {dt} → Price: {price}")
                self.valuation_price = price
                return price

        # If no exact or future date found, return the last known price
        print(f"⚠️ No future date found, using last available date: {self.dates[-1]} → Price: {self.prices[-1]}")
        return self.prices[-1]



    def estimate_params(self):
        """
        Estimate drift (mu) and volatility (sigma) using historical mean and standard deviation of log returns.
        """
        if self.log_returns is None:
            raise ValueError("No log returns data available. Fetch historical data first.")

        # Compute drift (μ) as the mean of log returns, annualized
        mu_annual = np.mean(self.log_returns) * 252  # Convert daily drift to annualized
        
        # Compute volatility (σ) as the standard deviation of log returns, annualized
        sigma_annual = np.std(self.log_returns) * np.sqrt(252)  # Convert daily volatility to annualized
        
        self.mu_est = mu_annual
        self.sigma_est = sigma_annual

        print(f"Estimated Mu (Drift): {self.mu_est:.4f} ({self.mu_est * 100:.2f}%)")
        print(f"Estimated Sigma (Volatility): {self.sigma_est:.4f} ({self.sigma_est * 100:.2f}%)")
        
        return self.mu_est, self.sigma_est
