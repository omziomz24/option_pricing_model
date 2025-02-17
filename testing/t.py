import yfinance as yf
import numpy as np

def calculate_annual_drift(ticker, start_date="2022-01-01", end_date="2025-02-14"):
    """
    Fetches stock data, calculates log returns, and computes the annualized drift percentage.
    
    :param ticker: Stock ticker symbol (e.g., "AAPL", "TSLA", "ALL.AX")
    :param start_date: Start date for historical data
    :param end_date: End date for historical data
    :return: Annualized drift percentage
    """
    try:
        # Download historical stock data
        df = yf.download(ticker, start=start_date, end=end_date)

        # Ensure data is not empty
        if df.empty:
            print(f"Error: No data found for {ticker}. Check the ticker symbol and date range.")
            return None

        # Select adjusted closing prices
        prices = df["Close"]

        # Compute log returns
        log_returns = np.log(prices / prices.shift(1)).dropna()

        # Calculate the drift (mean log return)
        drift = log_returns.mean()

        # Convert to annualized percentage and extract the scalar value
        annual_drift_percentage = float(drift * 252 * 100)

        print(f"\n📈 Stock: {ticker}")
        print(f"📅 Date Range: {start_date} to {end_date}")
        print(f"📊 Annualized Drift: {annual_drift_percentage:.2f}%")

        return annual_drift_percentage

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Example usage: Replace "ALL.AX" with any stock symbol you want
if __name__ == "__main__":
    ticker_symbol = input("Enter a stock ticker (e.g., AAPL, TSLA, MSFT, ALL.AX): ").upper()
    calculate_annual_drift(ticker_symbol)
