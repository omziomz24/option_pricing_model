# Error message for model failures (NOT IN USE)
MODEL_ERROR_MSG = """
<div style="
    border: 2px solid red; 
    background-color: #ffe6e6; 
    padding: 15px; 
    border-radius: 10px; 
    text-align: center; 
    width: auto;
    font-family: Arial, sans-serif;">
    <h3 style="color: red; margin: 5px 0;">Error</h3>
    <p style="font-size: 18px; font-weight: bold; color: black; margin: 5px 0;">
        An unexpected error has occurred.<br>
        Please check the inputs and try again.
    </p>
</div>
"""

# In the top of the website for people to learn about the model
MODEL_DESCRIPTION = """
## Option Pricing Model  

An **option** is a financial derivative that gives the holder the right, but not the obligation, to buy or sell an underlying asset at a predetermined price before or at expiration. Options are widely used for hedging, speculation, and portfolio management.

### Supported Assets:
This model supports **any asset listed on the ASX 200 or S&P 500**, allowing users to analyze and price options for a wide range of stocks and indices.

### Parameters of an Option:
- **Strike Price:** The price at which the option can be exercised.
- **Underlying Price:** *(Automatically calculated by the model)* – The current price of the asset.
- **Time to Expiration:** The time remaining until the option expires.
- **Volatility:** *(Automatically calculated by the model)* – The measure of price fluctuations of the underlying asset, estimated using historical data.
- **Risk-Free Rate:** *(Automatically calculated by the model)* – The return on a risk-free investment (e.g., government bonds), based on current market data.
- **Option Type:** Call (right to buy) or Put (right to sell).

### How This Model Works:
This model uses **Geometric Brownian Motion (GBM)** to simulate the future price movements of the underlying asset. GBM is a widely used mathematical model that assumes:
- The asset price follows a **stochastic process** with continuous paths.
- Returns are normally distributed.
- Future prices depend on a drift term (expected return) and a random shock (volatility).

To estimate the fair value of an option, the model employs **Monte Carlo simulations**:
1. It generates thousands of possible future price paths using GBM.
2. It calculates the option's payoff for each scenario.
3. The final option price is obtained by taking the average discounted payoff.

By leveraging Monte Carlo methods, this approach provides a flexible and robust way to price options, especially for cases where analytical solutions are difficult to derive.

Try adjusting the parameters to see how they affect option pricing for assets on the **ASX 200 or S&P 500**!
"""

<<<<<<< HEAD
=======
# LinkedIn Plug
LINKEDIN_FLEX = """
                <div style="
                    border: 2px solid #0077B5; 
                    border-radius: 10px; 
                    padding: 7.5px; 
                    display: flex; 
                    align-items: center;
                    justify-content: center;
                    width: 100%;
                ">
                    <img src="https://upload.wikimedia.org/wikipedia/commons/c/ca/LinkedIn_logo_initials.png" 
                        width="30" style="margin-right: 10px;">
                    <a href="https://www.linkedin.com/in/omaramin23" target="_blank" 
                    style="font-size: 16px; text-decoration: none; color: #0077B5; font-weight: bold;">
                        Connect with me on LinkedIn
                    </a>
                </div>
                """

>>>>>>> 5bd147f94 (Updated existing files)
# Option price display (placeholders used instead of f-string)
OPTION_PRICE_DISPLAY = """
<div style="display: flex; justify-content: center; gap: 15px;">
    <div style="border: 2px solid #87CEEB; background-color: #00509d; padding: 10px; border-radius: 10px; text-align: center; width: 250px; height: auto;">
        <h3 style="color: white; margin: 3px 0;">Call Option Price</h3>
        <p style="font-size: 22px; font-weight: bold; color: white; margin: 3px 0;">${call_price}</p>
    </div>
    <div style="border: 2px solid #87CEEB; background-color: #00509d; padding: 10px; border-radius: 10px; text-align: center; width: 250px; height: auto;">
        <h3 style="color: white; margin: 3px 0;">Put Option Price</h3>
        <p style="font-size: 22px; font-weight: bold; color: white; margin: 3px 0;">${put_price}</p>
    </div>
</div>
"""

# Used in the option greek expander to explain what they are
OPTION_GREEK_DESCRIPTION = """
                            **Option Greeks Overview**
                            Option Greeks measure how an option’s price reacts to changes in stock price, volatility, time, and interest rates.

                            🔹 **Delta (Δ)**
                                – Sensitivity to stock price. 
                                - Call Delta (0 to 1), Put Delta (-1 to 0).
                                - Higher Delta → Option moves closely with stock.

                            🔹 **Gamma (Γ)**
                                – Sensitivity of Delta.
                                - Higher Gamma → Delta changes rapidly.

                            🔹 **Theta (Θ)**
                                – Time decay.
                                - Higher Theta → Faster value loss as expiration nears.
                                - Bad for buyers, good for sellers.

                            🔹 **Vega (ν)**
                                – Sensitivity to volatility.
                                - Higher Vega → More impact from volatility changes.

                            🔹 **Rho (ρ)**
                                – Sensitivity to interest rates.
                                - Calls have positive Rho, Puts have negative Rho.

                            **Key Insights**
                            - **Buyers** want high Delta, high Vega, and low Theta.
                            - **Sellers** prefer low Delta, low Vega, and high Theta.
                            """