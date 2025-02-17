from .utils import *
from .option_strike import Strike
from .stochastic_process import Stochastic_Process
from .rfr_projection import RFR_Projection
from .volaility_model_MLE import Return_Volatility_Minimisation
from .volatility_model_ML import ML_Volatility_Model
from .euro_option_simulation import European_Option_Simulation

def supress_warnings():
    # This prevents cmdstanpy from printing "Chain [1] start processing"
    cmdstanpy_logger = logging.getLogger("cmdstanpy")
    cmdstanpy_logger.propagate = False
    cmdstanpy_logger.disabled = True

    # Suppress pandas SettingWithCopyWarning
    pd.options.mode.chained_assignment = None

    # Supress pandas Performance Warnings
    warnings.simplefilter(action="ignore", category=PerformanceWarning)

    # Supress Scikit Future Warnings
    warnings.simplefilter(action="ignore", category=FutureWarning)

    # Setup info logging format
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    # Suppress Prophet's INFO logs
    logging.getLogger("prophet").setLevel(logging.WARNING)

def get_end_date(start_date, tte):
    # Compute end date correctly (pass as a string)
    end_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=tte)).strftime("%Y-%m-%d")

    return end_date

def get_stock_data(ticker, start, end, price_column='Adj Close'):
    """
    Retrieve historical stock price data using yfinance.
    """

    # Log
    logging.info("Retrieving historical stock data")

    data = yf.download(ticker, start=start, end=end, progress=True)

    # If MultiIndex, drop the second level (ticker name)
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.droplevel(1)  # Remove 'MSFT' part

    if data.empty:
        raise ValueError(f"No data found for ticker: {ticker}")
    
    if price_column not in data.columns:
        if 'Close' in data.columns:
            price_column = 'Close'
        else:
            raise ValueError(f"Neither '{price_column}' nor 'Close' found in data. Couldn't find stock data!")

    return [data, start, end, price_column]

<<<<<<< HEAD
def get_rfr(start_date, tte):
    # Log
    logging.info("Projecting and retrieving risk free rate (AUS data)")
=======
def get_rfr(start_date, tte, suffix: str):
    # Log
    logging.info("Projecting and retrieving risk free rate")
>>>>>>> 5bd147f94 (Updated existing files)
    
    end_date = get_end_date(start_date, tte)
    
    # Set up risk free rate forecast
    rfr = RFR_Projection(365)
<<<<<<< HEAD
    rfr.forecast()
=======
    rfr.forecast(suffix)
>>>>>>> 5bd147f94 (Updated existing files)
    rfr_forecast_results = rfr.get_forecast()

    # Filter for appropriate risk free rates
    rfr_range = rfr_forecast_results[
    (rfr_forecast_results['Date'] >= start_date) &
    (rfr_forecast_results['Date'] <= end_date)
    ]
    # Calculate present value of price of call option
    rfr = np.average(rfr_range['Rate'])

    return [rfr, rfr_range]

def get_volatility(start_date, stock_data: list, minimiser: Return_Volatility_Minimisation, tte, ticker):
    # Log
    logging.info("Modelling volatility of asset")

    end_date = get_end_date(start_date, tte)

    # Fetch historical data first
    minimiser.fetch_historical_volatility(ticker, stock_data=stock_data[0], start=stock_data[1], end=stock_data[2], price_column=stock_data[3])
        
    # Usage
    ml_vol_model = ML_Volatility_Model(ticker, start_date, end_date)
    ml_vol_model.train_model(stock_data[0])

    # Predict future volatility
    future_vol = ml_vol_model.predict_volatility()

    print(f"Adjusted Predicted Volatility: {future_vol:.4f} ({future_vol*100:.2f}%)")

    return future_vol

def get_spot_price(start_date, minimiser):
    # Convert start_date to a pandas Timestamp if it's a string
    if isinstance(start_date, str):
        start_date = pd.Timestamp(start_date)

    # Log
    logging.info(f"Retrieving spot price of asset at {start_date.strftime('%Y-%m-%d')}")

    if len(minimiser.dates) > 0:
        # Convert minimiser.dates to pandas Timestamp if they are strings
        minimiser.dates = [pd.Timestamp(d) if isinstance(d, str) else d for d in minimiser.dates]

        # Find the closest date to start_date
        adjusted_start_date = min(minimiser.dates, key=lambda d: abs(d - start_date))
        
        if start_date.strftime('%Y-%m-%d') != adjusted_start_date.strftime('%Y-%m-%d'):
            logging.warning(f"Adjusting start date from {start_date.strftime('%Y-%m-%d')} "
                            f"to {adjusted_start_date.strftime('%Y-%m-%d')} since no stock data was found at {start_date.strftime('%Y-%m-%d')}")
    else:
        logging.error("No historical data available!")
        return None

    # Fetch Valuation Price using the closest available date
    valuation_price = minimiser.get_valuation_price(adjusted_start_date)

    return valuation_price



def display_option_pricing_summary(
    ticker, start_date, tte, strike, stock_data_start, stock_data_end, 
    rfr, spot_price, future_volatility, call_option_price, put_option_price
):
    """Displays a formatted summary of the option pricing calculations in a table format."""

    # ANSI escape codes for formatting
    BOLD = "\033[1m"
    RESET = "\033[0m"
    MAGENTA = "\033[35m"
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    YELLOW = "\033[1;33m"

    # Calculate Expiry Date (Start Date + TTE Days)
    expiry_date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=tte)).strftime("%Y-%m-%d")

    print(f"\n{BOLD}{BLUE}--- OPTION PRICING TOOL INPUTS ---{RESET}")

    print(f"{BOLD}{CYAN}Stock Data for ${ticker}{RESET}")
    print(f"  {'Stock Data Range:':<25} {stock_data_start} to {stock_data_end}")

    print(f"{BOLD}{CYAN}Risk-Free Rate and Volatility{RESET}")
    print(f"  {'Risk-Free Rate:':<25} {BOLD}{MAGENTA}{rfr*100:.3f}%{RESET}")
    print(f"  {'Predicted Volatility:':<25} {BOLD}{MAGENTA}{future_volatility*100:.2f}%{RESET}")

    print(f"{BOLD}{CYAN}TTE and Dates{RESET}")
    print(f"  {'Start Date:':<25} {start_date}")
    print(f"  {'Expiry Date:':<25} {expiry_date}")
    print(f"  {'Time to Expiry (TTE):':<25} {tte} days")

    print(f"{BOLD}{CYAN}Strike and Spot{RESET}")
    print(f"  {'Strike Price:':<25} {YELLOW}${strike:.2f}{RESET}")
    print(f"  {'Spot Price:':<25} {YELLOW}${spot_price:.3f}{RESET}")
    
    print(f"{BOLD}{RED}{'Call Option Price:':<27} ${call_option_price:.3f}{RESET}")
    print(f"{BOLD}{RED}{'Put Option Price:':<27} ${put_option_price:.3f}{RESET}")
    
    #print(f"\n{BOLD}{GREEN}--- PROCESS COMPLETED SUCCESSFULLY ---{RESET}\n")

def get_available_tickers():
    """Returns all tickers for S&P500 and the ASX200 in a list"""
    # Fetch S&P 500 tickers
    sp500_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    sp500_tickers = pd.read_html(sp500_url)[0]['Symbol'].tolist()

    # Fetch ASX 200 tickers
    asx200_url = "https://en.wikipedia.org/wiki/S%26P/ASX_200"
    asx200_tickers = pd.read_html(asx200_url)[2]['Code'].tolist()
    asx200_tickers_AX = [ticker + ".AX" for ticker in asx200_tickers]
    

    # Combine tickers and sort them
    all_tickers = sorted(set(sp500_tickers + asx200_tickers_AX))

    return all_tickers

def format_value(symbol: str, value: float, decimal_places: int):
    """
    Format a given float value as a percentage or currency based on the specified symbol.

    This function takes a numerical value and formats it as either:
    - A percentage ("%") by multiplying it by 100 and appending a "%" sign.
    - A currency ("$") by prefixing it with "$".
    - If an unrecognized symbol is provided, it returns the unformatted value.

    Parameter
    ----------
    symbol : str
        The format symbol to apply. Use "%" for percentages and "$" for currency.
    value : float
        The numerical value to be formatted.
    decimal_places : int
        The number of decimal places to round the formatted value to.

    Returns
    -------
    str
        The formatted string if the symbol is "%" or "$".
    float
        The original unformatted value if the symbol is not recognized.

    Examples
    ---------
    >>> format_value("%", 0.12345, 3)
    '12.345%'

    >>> format_value("$", 1234.567, 2)
    '$1234.57'

    >>> format_value("€", 100, 2)  # Unsupported symbol returns original value
    100
    """
    if symbol == "%":
        return "{:.{}f}%".format(float(value * 100), decimal_places)
    elif symbol == "$":
        return "${:.{}f}".format(float(value), decimal_places)
    else:
        return value  # Return unformatted value if symbol is not recognized


<<<<<<< HEAD
def run_pricing_model(ticker: str, start_date: str, tte: int, strike: float, stock_data_start="2022-01-01", stock_data_end="2025-03-30", simulations=10000):
=======
def run_pricing_model(ticker: str, start_date: str, tte: int, strike: float, stock_data_start: str = "2022-01-01", stock_data_end: str = "2025-03-30", rfr_suffix: str = "AU-10", simulations: int = 10000):
>>>>>>> 5bd147f94 (Updated existing files)
    """
    Simulates option pricing for a European call/put option using a Monte Carlo method 
    based on Geometric Brownian Motion (GBM).

    This function retrieves historical stock data, estimates the risk-free rate and volatility, 
    and then runs a Monte Carlo simulation to determine the fair value of European-style options. 
    The calculation is parallelized for efficiency.

    Parameters
    ----------
    ticker : str
        The stock ticker symbol for the underlying asset.
    start_date : str
        The valuation date for the option pricing model.
    tte : int
        Time to expiry in days.
    strike : float
        The strike price of the option.
    stock_data_start : str, optional
        The start date for retrieving historical stock data (default: "2022-01-01").
    stock_data_end : str, optional
        The end date for retrieving historical stock data (default: "2025-03-30").
<<<<<<< HEAD
=======
    rfr_suffix : str, optional
        Which government bond yields to use for risk free rate forecast (default: "AU-10").
>>>>>>> 5bd147f94 (Updated existing files)
    simulations : int, optional
        The number of Monte Carlo simulations to run (default: 10,000).

    Returns
    -------
    dict
        A dictionary containing:
        - "ticker" (str): The stock ticker.
        - "start_date" (str): The date when the option pricing is evaluated.
        - "time to expiry" (int): The number of days until the option expires.
        - "strike" (float): The option's strike price.
        - "stock data start" (str): The start date for historical stock data.
        - "stock data end" (str): The end date for historical stock data.
        - "risk free rate" (float): The projected risk-free interest rate.
        - "spot price" (float): The estimated current price of the underlying asset.
        - "volatility" (float): The estimated future volatility of the underlying asset.
        - "call price" (float): The estimated fair value of the European call option.
        - "put price" (float): The estimated fair value of the European put option.
        - "stock prices" (NDArray): Contains all historic stock price data and associated dates
        - "stock dates" (NDArray): Contains all the assocaited dates for the stock prices
        - "all simulations" (list): Contains lists of all geometric brownian motion stock price simulations
<<<<<<< HEAD
=======
        - "rfr dataset" (str): Contains the code of which dataset risk free rate was generated from
>>>>>>> 5bd147f94 (Updated existing files)
    """

    # Step 1: Retrieving historical stock data
    status_placeholder = st.empty()
    calculation_status = status_placeholder.status("🧮 Calculating option price...", expanded=True)

    with calculation_status:
            st.write("📊 Retrieving historical stock data...")
    calculation_status.update(state="running")

    supress_warnings()

    # Initialise the minimiser model
    minimiser = Return_Volatility_Minimisation(dt=1/252)

    # Initialise input variables 
    stock_data = get_stock_data(ticker, start=stock_data_start, end=stock_data_end)


    # Step 2: Projecting market risk free rate
    with calculation_status:
            st.write("📈 Analyzing market risk free rate...")
    calculation_status.update(state="running")

<<<<<<< HEAD
    rfr, rfr_range = get_rfr(start_date, tte)
=======
    rfr, rfr_range = get_rfr(start_date, tte, rfr_suffix)
>>>>>>> 5bd147f94 (Updated existing files)
    print(f"Risk Free Rate: {rfr:.4f}")
    # Prints the last 4 risk free rates if we want to view it
    #print(rfr_range.tail(4))
    
    # Step 3: Analyse asset volatility
    with calculation_status:
            st.write("📈 Analyzing asset volatility rate...")
    calculation_status.update(state="running")

    future_volatility = get_volatility(start_date, stock_data, minimiser, tte, ticker)
    
    # Need to put spot price calculation here because of how things are initalised above
    spot_price = get_spot_price(start_date, minimiser)
    print(f"Spot Price: ${spot_price:.3f}")

    # Step 4: Running monte carlo simulations
    with calculation_status:
            st.write("🎲 Running Simulations...")
    calculation_status.update(state="running")

    logging.info("Now running stochastic differential equations to calculate option price")
    
    simulation = European_Option_Simulation(
        stochastic_process_type="GBM",
        strike=Strike(strike),
        sims=simulations,
        initial_price=spot_price,
        drift=rfr,
        delta_t=1/365,
        volatility=future_volatility,
        tte=tte/365,
        rfr_appropriate_dates=rfr_range
    )

    # Run simulations with multiprocessing
    call_price, put_price, all_simulations = simulation.run_multiprocessing(20)
    print(f"Call Option Price: ${call_price:.3f}")
    print(f"Call Option Price: ${put_price:.3f}")

    calculation_status.update(label="🧮 Model results loading...", state="running") 

    # Display results summary in terminal
    logging.info("\033[1;32m--Finished Model--\033[0m")
    display_option_pricing_summary(
        ticker, start_date, tte, strike, stock_data_start, stock_data_end, 
        rfr, spot_price, future_volatility, call_price, put_price
    )

    return {
        "ticker": ticker,
        "start_date": start_date,
        "time to expiry": tte,
        "strike": strike,
        "stock data start": stock_data_start,
        "stock data end": stock_data_end,
        "risk free rate": rfr,
        "spot price": spot_price,
        "volatility": future_volatility,
        "call price": call_price,
        "put price": put_price,
        "stock prices": minimiser.prices,
        "stock dates": minimiser.dates,
        "all simulations": all_simulations,
<<<<<<< HEAD
        "calculation status": calculation_status
=======
        "calculation status": calculation_status,
        "rfr dataset": rfr_suffix
>>>>>>> 5bd147f94 (Updated existing files)
    }

def calculate_greeks(option_type: str, S: float, K: float, T: float, r: float, sigma: float, decimals: int = 4):
    """
    Compute the Greeks for a European call or put option using the Black-Scholes model.

    Parameters
    ----------
    option_type : str
        Type of the option: "call" for a call option, "put" for a put option.
    S : float
        Current stock price (Spot price).
    K : float
        Strike price of the option.
    T : float
        Time to expiry (in years).
    r : float
        Risk-free interest rate (as a decimal, e.g., 0.05 for 5%).
    sigma : float
        Volatility of the underlying asset (as a decimal, e.g., 0.2 for 20%).
    decimals : int (Default = 4)
        How many decimals you want to round for use in the format_value() function

    Returns
    -------
    dict
        A dictionary containing:
        - "Delta" (float): Sensitivity to stock price changes.
        - "Gamma" (float): Sensitivity of Delta to stock price changes.
        - "Theta" (float): Time decay of the option price.
        - "Vega" (float): Sensitivity to volatility changes.
        - "Rho" (float): Sensitivity to interest rate changes.

    Example
    -------
    >>> calculate_greeks("call", 100, 100, 1, 0.05, 0.2)
    {'Delta': 0.6368, 'Gamma': 0.0198, 'Theta': -0.0176, 'Vega': 0.3973, 'Rho': 0.5323}
    """
    d1 = (np.log(S / K) + (r + (sigma ** 2) / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    delta = si.norm.cdf(d1) if option_type.lower() == "call" else si.norm.cdf(d1) - 1
    gamma = si.norm.pdf(d1) / (S * sigma * np.sqrt(T))
    theta = (- (S * si.norm.pdf(d1) * sigma) / (2 * np.sqrt(T))) - (r * K * np.exp(-r * T) * si.norm.cdf(d2)) if option_type.lower() == "call" else (- (S * si.norm.pdf(d1) * sigma) / (2 * np.sqrt(T))) + (r * K * np.exp(-r * T) * si.norm.cdf(-d2))
    vega = S * si.norm.pdf(d1) * np.sqrt(T)
    rho = K * T * np.exp(-r * T) * si.norm.cdf(d2) if option_type == "call" else -K * T * np.exp(-r * T) * si.norm.cdf(-d2)

    return {
        "Delta": ("%", decimals, delta),
        "Gamma": ("%", decimals, gamma),
        "Theta": ("%", decimals, theta/365),
        "Vega": ("%", decimals, vega/100),
        "Rho": ("%", decimals, rho/100)
    }
