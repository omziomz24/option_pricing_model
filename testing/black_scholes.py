# Re-import necessary libraries
import numpy as np
import scipy.stats as si

# Define Black-Scholes function
def black_scholes(S, K, T, r, sigma, option_type="call"):
    """
    Calculate the Black-Scholes price of a European call or put option.

    Parameters:
    S : float : Current stock price
    K : float : Strike price
    T : float : Time to expiration (in years)
    r : float : Risk-free rate (as a decimal)
    sigma : float : Volatility of the stock (as a decimal)
    option_type : str : "call" for a call option, "put" for a put option

    Returns:
    float : Option price
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "call":
        option_price = (S * si.norm.cdf(d1)) - (K * np.exp(-r * T) * si.norm.cdf(d2))
    elif option_type == "put":
        option_price = (K * np.exp(-r * T) * si.norm.cdf(-d2)) - (S * si.norm.cdf(-d1))
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")

    return option_price

# Given Microsoft (MSFT) option parameters
S_msft = 334.09  # Current stock price
K_msft = 330      # Strike price
T_msft = 183 / 365  # Time to expiration in years
r_msft = 0.0367   # Risk-free rate (3.67%)
sigma_20 = 0.20   # Given volatility (20%)
sigma_25 = 0.25   # Adjusted volatility (25%)
sigma_30 = 0.30   # Adjusted volatility (30%)

# Calculate Black-Scholes call option prices with different volatilities
option_price_20 = black_scholes(S_msft, K_msft, T_msft, r_msft, sigma_20, option_type="call")
option_price_25 = black_scholes(S_msft, K_msft, T_msft, r_msft, sigma_25, option_type="call")
option_price_30 = black_scholes(S_msft, K_msft, T_msft, r_msft, sigma_30, option_type="call")

# Output the results
option_prices = {
    "20% Volatility": option_price_20,
    "25% Volatility": option_price_25,
    "30% Volatility": option_price_30
}

print(option_prices)
