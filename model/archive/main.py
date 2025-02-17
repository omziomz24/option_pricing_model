from model import *

# Need to investigate better way to look at future stock prices? Random walk not really working maybe change drift to other than rfr?

if __name__ == "__main__":

    ##################################### INPUTS #####################################
    ticker = "CBA.AX"
    start_date = "2025-02-15"
    tte = 5
    strike = 124.01

    stock_data_start = "2022-01-01"
    stock_data_end = "2025-03-30"
    
    simulations = 10000

    run_pricing_model(ticker, start_date, tte, strike)
    ##################################################################################

    # def run_pricing_model(ticker, start_date, tte, strike, stock_data_start="2022-01-01", stock_data_end="2025-03-30", simulations=10000):
    #     supress_warnings()

    #     # Initialise the minimiser model
    #     minimiser = Return_Volatility_Minimisation(dt=1/252)

    #     # Initialise input variables 
    #     stock_data = get_stock_data(ticker, start=stock_data_start, end=stock_data_end)
    #     rfr, rfr_range = get_rfr(start_date, tte)
    #     # Prints the last 4 risk free rates if we want to view it
    #     #print(rfr_range.tail(4))
    #     print(f"Risk Free Rate: {rfr:.4f}")
    #     future_volatility = get_volatility(start_date, stock_data, minimiser, tte, ticker)
    #     spot_price = get_spot_price(start_date, minimiser)   
    #     print(f"Spot Price: ${spot_price:.3f}")
        
    #     # Setup simulation
    #     logging.info("Now running stochastic differential equations to calculate option price")
    #     simulation = European_Option_Simulation(
    #         stochastic_process_type="GBM",
    #         strike=Strike(strike),
    #         sims=simulations,
    #         initial_price=spot_price,
    #         drift=rfr,
    #         delta_t=1/365,
    #         volatility=future_volatility,
    #         tte=tte/365,
    #         rfr_appropriate_dates=rfr_range
    #     )

    #     # Run simulations with multiprocessing
    #     call_price, put_price, all_simulations = simulation.run_multiprocessing(20)
    #     print(f"Call Option Price: ${call_price:.3f}")
    #     print(f"Call Option Price: ${put_price:.3f}")

    #     # Display results summary in terminal
    #     logging.info("\033[1;32m--Finished Model--\033[0m")
    #     display_option_pricing_summary(
    #         ticker, start_date, tte, strike, stock_data_start, stock_data_end, 
    #         rfr, spot_price, future_volatility, call_price, put_price
    #     )

    #     # try:
    #     #     # Plot the simulations
    #     #     plot = str(input(f"\n\033[1mPlot simulations and stock price (Y/N):\033[0m ")).upper()
    #     #     if plot == "Y":
    #     #         Multi_Plot_Navigator(simulation=simulation,
    #     #                         minimiser=minimiser,
    #     #                         ticker=ticker,
    #     #                         all_simulations=all_simulations,
    #     #                         call_price=call_price,
    #     #                         put_price=put_price,
    #     #                         spot_price_0=spot_price)
    #     # except KeyboardInterrupt:
    #     #     print("\n\nScript interrupted by user. Exiting gracefully...\n")
    #     #     exit(0)  # Exits the script without error

    #     return "Done!"