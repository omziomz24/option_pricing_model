# 🏦 Option Pricing Tool

A powerful **Python-based option pricing tool** that leverages **Monte Carlo simulations** and **Geometric Brownian Motion (GBM)** to estimate the fair value of options. Built with **Streamlit**, this model provides a **web-based interface** for easy and intuitive option pricing.

🚀 **Try it live here:** [**Option Pricing Web App**](https://omar-option-pricer.streamlit.app/)

---

## 📌 Features

- 📈 **Supports ASX 200 & S&P 500 Assets** – Analyze options for a wide range of stocks and indices.
- 📊 **Monte Carlo Simulations** – Generates thousands of price paths to estimate option values.
- 🏦 **Stochastic Processes** – Models future asset price movements with geometric Brownian motions, arithmetic Brownian motions and multifractal model of asset returns.
- 🔢 **Automatic Data Retrieval** – Fetches real-time underlying prices, volatility, and risk-free rates.
- 🎯 **Flexible Option Parameters** – Customize strike price, expiration date, and option type (Call/Put).

---

## 📘 Understanding Options

An **option** is a financial derivative that gives the holder the **right, but not the obligation**, to buy or sell an underlying asset at a predetermined price before or at expiration. Options are widely used for **hedging, speculation, and portfolio management**.

### 📝 Option Parameters:
- **Strike Price** – The price at which the option can be exercised.
- **Underlying Price** *(Auto-calculated)* – The current market price of the asset.
- **Time to Expiration** – The remaining time until the option expires.
- **Volatility** *(Auto-calculated)* – Historical price fluctuation estimate.
- **Risk-Free Rate** *(Auto-calculated)* – Market-based return on a risk-free investment.
- **Option Type** – Call (right to buy) or Put (right to sell).

---

## 🏗️ How It Works

This tool simulates future price movements of the **underlying asset** using **Geometric Brownian Motion (GBM)**, a stochastic model that assumes:
- The asset price follows a **continuous-time process**.
- Returns are **normally distributed**.
- Prices evolve based on **drift (expected return) and random volatility**.

### 🎲 Monte Carlo Simulation:
1. Generates thousands of potential future price paths.
2. Computes the option’s payoff for each path.
3. Averages the discounted payoffs to determine the option’s fair value.

---

## 📢 Try It Now!
🔗 **[Launch the Web App](https://omar-option-pricer.streamlit.app/)** and experiment with different parameters to see how option pricing changes.

For reference, check out available ASX options:  
[🔗 **ASX Single Stock Equity Derivatives**](https://www.asx.com.au/markets/trade-our-derivatives-market/derivatives-market-prices/single-stock-derivatives)

---

## 🛠️ Installation & Usage (Local)
To run the model locally, install dependencies and launch the Streamlit app.

### 📌 Requirements:
- Python 3.x
- `streamlit`
- `numpy`
- `pandas`
- `matplotlib`
- `yfinance` (for real-time data)

### 🔧 Installation:
```bash
git clone https://github.com/omziomz24/option_pricing_model.git
cd option_pricing_model
pip install -r requirements.txt
```

### 🚀 Run the Web App Locally:
```bash
streamlit run app.py
```

# 📜 License
This project is open-source and available under the MIT License.

# 👨‍💻 About the Developer
📧 Contact: omziomz2336@outlook.com