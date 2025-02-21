from model import *

if __name__ == "__main__":
    st.title("Option Pricing Model")
    # Spacer between the title and the rest of the information
    st.write(" ")

    with st.expander("What are options and what is this model?", expanded=False, icon="📋"):
        st.markdown(MODEL_DESCRIPTION)
    
    with st.expander("Stock Candlesticks and Indicators", expanded=False, icon="🕯️"):
        # Select stock ticker
        candle_ticker = st.selectbox(
            "Select or search ticker",
            all_tickers,
            index=None,
            placeholder="Start typing...",
            key="candle_stick_selector"
        )

        # Date range selection
        candle_start_date = st.date_input("Start Date", value=pd.to_datetime("2024-01-01"))
        candle_end_date = st.date_input("End Date", value=pd.to_datetime("today"))

        if "stock_data" not in st.session_state or st.session_state["last_ticker"] != candle_ticker:
            if candle_ticker:
                st.session_state["stock_data"] = fetch_stock_data(candle_ticker, candle_start_date, candle_end_date)
                st.session_state["last_ticker"] = candle_ticker

        # Retrieve stock data from session state
        candle_prices_df = st.session_state.get("stock_data", pd.DataFrame())

        # Fetch stock data only after user selects a ticker
        if not candle_prices_df.empty:
            # Prevent API call when dates are invalid
            if candle_start_date >= candle_end_date:
                st.error("❌ The start date must be before the end date. Please select a valid range.")
            else:
                candle_prices_df = st.session_state.get("stock_data", pd.DataFrame())

                if candle_prices_df.empty:
                    st.warning(f"⚠️ No data found for {candle_ticker}. Try a different ticker or date range.")
                else:
                    # Reset index to move Date from Index to Column
                    candle_prices_df = candle_prices_df.reset_index()

                    # If MultiIndex exists, extract the correct column names
                    if isinstance(candle_prices_df.columns, pd.MultiIndex):
                        candle_prices_df.columns = candle_prices_df.columns.get_level_values(0)

                    # Rename the first column to "Date" if needed
                    if candle_prices_df.columns[0] != "Date":
                        candle_prices_df.rename(columns={candle_prices_df.columns[0]: "Date"}, inplace=True)

                    candle_prices_df["Date"] = pd.to_datetime(candle_prices_df["Date"])

                    # Checkboxes for graph Indicators
                    st.subheader("📌 Select Indicators to Display:")
                    sma_50 = st.checkbox("SMA (50)")
                    sma_200 = st.checkbox("SMA (200)")
                    ema_20 = st.checkbox("EMA (20)")
                    bollinger = st.checkbox("Bollinger Bands")

                    # Collect selected indicators
                    selected_indicators = []
                    if sma_50:
                        selected_indicators.append("SMA (50)")
                    if sma_200:
                        selected_indicators.append("SMA (200)")
                    if ema_20:
                        selected_indicators.append("EMA (20)")
                    if bollinger:
                        selected_indicators.append("Bollinger Bands")

                    # Add selected indicators
                    candle_prices_df = add_indicators(candle_prices_df, selected_indicators)

                    candle_graph = go.Figure()

                    candle_graph.add_trace(go.Candlestick(
                        x=candle_prices_df["Date"].round(2),
                        open=candle_prices_df["Open"].round(2),
                        high=candle_prices_df["High"].round(2),
                        low=candle_prices_df["Low"].round(2),
                        close=candle_prices_df["Close"].round(2),
                        name="Candlestick",
                        increasing_line_color="lime",
                        decreasing_line_color="red",
                    ))

                    # Overlay Selected Indicators
                    if "SMA (50)" in selected_indicators:
                        candle_graph.add_trace(go.Scatter(
                            x=candle_prices_df["Date"],
                            y=candle_prices_df["SMA_50"],
                            mode="lines",
                            name="SMA (50)",
                            line=dict(color="blue")
                        ))

                    if "SMA (200)" in selected_indicators:
                        candle_graph.add_trace(go.Scatter(
                            x=candle_prices_df["Date"],
                            y=candle_prices_df["SMA_200"],
                            mode="lines",
                            name="SMA (200)",
                            line=dict(color="purple")
                        ))

                    if "EMA (20)" in selected_indicators:
                        candle_graph.add_trace(go.Scatter(
                            x=candle_prices_df["Date"],
                            y=candle_prices_df["EMA_20"],
                            mode="lines",
                            name="EMA (20)",
                            line=dict(color="orange")
                        ))

                    if "Bollinger Bands" in selected_indicators:
                        candle_graph.add_trace(go.Scatter(
                            x=candle_prices_df["Date"],
                            y=candle_prices_df["BB_Upper"],
                            mode="lines",
                            name="BB Upper",
                            line=dict(color="gray", dash="dot")
                        ))
                        candle_graph.add_trace(go.Scatter(
                            x=candle_prices_df["Date"],
                            y=candle_prices_df["BB_Lower"],
                            mode="lines",
                            name="BB Lower",
                            line=dict(color="gray", dash="dot")
                        ))

                    # Customize Layout
                    candle_graph.update_layout(
                        title=f"     📈 {candle_ticker} Candlestick Chart",
                        xaxis_title="Date",
                        yaxis_title="Stock Price",
                        xaxis_rangeslider_visible=False,
                        template="plotly_dark",
                        hovermode="x unified",
                        dragmode="pan",
                        plot_bgcolor="#1e1e1e",
                        paper_bgcolor="#1e1e1e",
                        font=dict(color="white")
                    )

                    # Display chart in Streamlit
                    st.plotly_chart(candle_graph, use_container_width=True)

    # When boolean becomes true the sidebar calculation is completed and will start updating main page
    update_main = False

    # Initalise model ouputs to reference anywhere
    call_price, put_price, risk_free_rate, spot_price, volatility,\
        historic_stock_price_data, historic_stock_price_dates, \
        all_simulations, calculation_loading_status \
         = None, None, None, None, None, None, None, None, None

    with st.sidebar:
        # Force side bar to be 400px wide to look nicer
        st.markdown(SIDEBAR_WIDTH, unsafe_allow_html=True)
        # Add linkedin flex with link to top of sidebar
        st.markdown(LINKEDIN_FLEX, unsafe_allow_html=True)

        st.title("💡 Price Options Here ↓")
        st.subheader("Enter Option Details")

        # User Inputs
        asset_ticker = st.selectbox("Select or search ticker", all_tickers, index=None, placeholder="Start typing...", key="ticker")
        strike_price = st.number_input("Strike price ($)", min_value=0.00, value=None, format="%.2f", )
        start_date = st.date_input("Select a start date")
        expiry_date = st.date_input("Select an expiry date", value=None)

        # Extra advanced user inputs
        with st.expander(label="⚙️ Click here for advanced settings", expanded=False) as advanced_settings_expander:
            MANUAL_risk_free_rate_dataset = st.selectbox("Use bond yields to project risk free rate", all_rfr_datasets, index=0)
            MANUAL_risk_free_rate = st.number_input("OR Manually input risk free rate (%)", min_value = 0.000, value=None, format="%.3f")
            MANUAL_volatility = st.number_input("Volatility (%)", min_value = 0.000, value=None, format="%.3f")
            MANUAL_stochastic_process = st.selectbox("Stochastic process", stochastic_processes, index=0)

        # Button to submit inputs and checks to see if inputs exist
        if st.button("Calculate Option Price"):
            # Resets side bar progress (if run without errors main page will be updated)
            update_main = False

            # Blank input checkers
            if not asset_ticker:
                st.error("Please select a ticker")
            elif not strike_price:
                st.error("Please enter a strike price")
            elif not start_date:
                st.error("Please enter a start date")
            elif not expiry_date:
                st.error("Please enter an expiry date")
            elif (expiry_date - start_date).days <= 0:
                st.error("Please input an expiry date which is later than the start date")
            else:
                time_to_expiry = (expiry_date - start_date).days

                try:
                    pricing_result = run_pricing_model(ticker=str(asset_ticker),
                                                    start_date=str(start_date),
                                                    tte=int(time_to_expiry),
                                                    manual_input_data=[
                                                                    MANUAL_volatility/100 if MANUAL_volatility is not None else None,
                                                                    MANUAL_risk_free_rate/100 if MANUAL_risk_free_rate is not None else None,
                                                                    MANUAL_stochastic_process if MANUAL_stochastic_process is not None else "Geometric Brownian Motion"
                                                                ],
                                                    strike=float(strike_price),
                                                    stock_data_start="2022-01-01",
                                                    stock_data_end="2025-03-30",
                                                    rfr_suffix=str(MANUAL_risk_free_rate_dataset),
                                                    simulations=10000)
                    
                    # Extract model outputs
                    call_price = pricing_result.get("call price", "N/A")
                    put_price = pricing_result.get("put price", "N/A")
                    risk_free_rate = pricing_result.get("risk free rate", "N/A")
                    spot_price = pricing_result.get("spot price", "N/A")
                    volatility = pricing_result.get("volatility", "N/A")
                    historic_stock_price_data = pricing_result.get("stock prices", "N/A")
                    historic_stock_price_dates = pricing_result.get("stock dates", "N/A")
                    all_simulations = pricing_result.get("all simulations", "N/A")
                    calculation_loading_status = pricing_result.get("calculation status", "N/A")
                    # Display the results in two red-outlined boxes
                    st.markdown(OPTION_PRICE_DISPLAY.format(call_price="{:.2f}".format(float(call_price)), put_price="{:.2f}".format(float(put_price))), unsafe_allow_html=True)
                    
                    update_main = True

                except Exception as e:
                    # Line is for debugging errors with run_pricing_model() only
                    # logging.error("", exc_info=True)
                    # Raise error if pricing model errors out (likely due to inputs being incorrect)
                    st.error("An unexpected error has occurred. Please check the inputs and try again.")

    if update_main:
        with calculation_loading_status:
            st.write("🔍 Displaying results")
        calculation_loading_status.update(state="running")

        result_loading_placeholder1 = st.empty()
        result_loading_placeholder1.text(" ")
        result_loading_placeholder_status1 = result_loading_placeholder1.status(label="Results still loading hang tight...", expanded=False, state="running")
        st.subheader("Results:")

        # Initalise variables to be referenced area
        unformatted_basic_results = {
                                    "Call Price": ("$", 2, call_price),
                                    "Put Price": ("$", 2, put_price),
                                    "Spot Price": ("$", 2, spot_price),
                                    "Risk-Free Rate": ("%", 3, risk_free_rate),
                                    "Volatility": ("%", 2, volatility)
                                    }
        
        greeks_call = calculate_greeks("call", spot_price, strike_price, time_to_expiry/365, risk_free_rate, volatility, 3)
        greeks_put = calculate_greeks("put", spot_price, strike_price, time_to_expiry/365, risk_free_rate, volatility, 3)

        # Display key basic option pricing results/parameters
        with st.expander("Option Pricing Basic Results/Parameters", expanded=False, icon="🔢"):
            
            formatted_basic_results = {
                key: format_value(symbol, value, decimal_places) for key, (symbol, decimal_places, value) in unformatted_basic_results.items()
            }
            basic_results = pd.DataFrame([formatted_basic_results])
            st.dataframe(basic_results, hide_index=True)
        
        with st.expander("Option Greeks", expanded=False, icon="⚖️"):
            
            option_greek_data_tab, option_greek_explanation_tab = st.tabs(["📊 Option Greeks", "📖 What are Option Greeks?"])

            with option_greek_data_tab:
                # st.subheader("📊 Option Greeks")
                
                formatted_call_greeks = {
                    key: format_value(symbol, value, decimal_places) for key, (symbol, decimal_places, value) in greeks_call.items()
                }
                formatted_put_greeks = {
                    key: format_value(symbol, value, decimal_places) for key, (symbol, decimal_places, value) in greeks_put.items()
                }

                greeks_call_results = pd.DataFrame([formatted_call_greeks])
                greeks_put_results = pd.DataFrame([formatted_put_greeks])

                st.text("Call Option Greeks")
                if call_price > 0.5:
                    st.dataframe(greeks_call_results, hide_index=True)
                else:
                    st.markdown("*No meaningful Greeks can be shown*")

                st.text("Put Option Greeks")
                if put_price > 0.5:
                    st.dataframe(greeks_put_results, hide_index=True)
                else:
                    st.markdown("*No meaningful Greeks can be shown*")

            with option_greek_explanation_tab:
                st.write(OPTION_GREEK_DESCRIPTION)

        with st.expander("Graphs", expanded=False, icon="📊"):
            historic_stock_price_graph_tab, option_varying_spot_graph_tab, monte_carlo_graph_tab \
                = st.tabs(["Historic Stock Prices", "Call/Put Prices", "Monte Carlo Simulations"])
            plt.style.use("seaborn-v0_8-darkgrid")

            with historic_stock_price_graph_tab:
                # historic_prices_data_frame = pd.DataFrame(historic_stock_price_data, columns=["Date", "Price"])
                # historic_prices_data_frame["Date"] = pd.to_datetime(historic_prices_data_frame["Date"])

                historic_prices_graph, historic_prices_ax = plt.subplots(figsize=(10,5))

                historic_prices_ax.plot(historic_stock_price_dates, historic_stock_price_data, label="Stock Price", color="blue")

                # Formatting
                historic_prices_ax.set_title(f"Stock Price History ${asset_ticker}", fontsize=14, fontweight="bold")
                historic_prices_ax.set_xlabel("Date", fontsize=12)
                historic_prices_ax.set_ylabel("Price", fontsize=12)
                historic_prices_ax.legend(loc="upper left", fontsize=12)
                historic_prices_ax.grid(True, linestyle="--", alpha=0.7)

                historic_prices_ax.set_xlim(historic_stock_price_dates.min(), historic_stock_price_dates.max())
                historic_prices_ax.xaxis.set_major_locator(mdates.AutoDateLocator())
                historic_prices_ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
                plt.xticks(rotation=37, fontsize=7)

                # Display the chart in Streamlit
                st.pyplot(historic_prices_graph)

            with option_varying_spot_graph_tab:
                option_prices_graph, option_prices_ax = plt.subplots(figsize=(10,5))

                spot_prices = np.linspace(0, 2 * strike_price, 100)
                call_values = np.maximum(spot_prices - strike_price, 0)  # Call: max(S_T - K, 0)
                put_values = np.maximum(strike_price - spot_prices, 0)   # Put: max(K - S_T, 0)

                # Plot Call & Put Option Payoffs
                call_line, = option_prices_ax.plot(spot_prices, call_values, label="Call Option", color='blue', linewidth=2)
                put_line, = option_prices_ax.plot(spot_prices, put_values, label="Put Option", color='red', linewidth=2)
                
                # Add vertical dotted line at spot price & legend update
                option_prices_ax.axvline(spot_price, color='black', linewidth=1, linestyle='--', label=f"Spot Price: ${spot_price:.2f}")
                option_prices_ax.set_title("European Call & Put Option Payoff at Expiration", fontsize=14)
                option_prices_ax.set_xlabel("Spot Price", fontsize=12)
                option_prices_ax.set_ylabel("Option Value", fontsize=12)
                option_prices_ax.legend(loc="upper right", fontsize=12, frameon=True, fancybox=True, edgecolor="black")
                option_prices_ax.grid(True)

                # Plot markers for model-predicted Call & Put prices
                actual_call_x, actual_put_x = spot_price, spot_price 
                actual_call_y, actual_put_y = call_price, put_price 

                option_prices_ax.scatter(actual_call_x, actual_call_y, color='blue', s=100, zorder=3)
                option_prices_ax.scatter(actual_put_x, actual_put_y, color='red', s=100, zorder=3)

                # Add annotations with arrows
                option_prices_ax.annotate(f"Call: ${actual_call_y:.2f}", xy=(actual_call_x, actual_call_y), 
                                            xytext=(actual_call_x + 5, actual_call_y + 5),
                                            arrowprops=dict(facecolor='blue', arrowstyle="->"), fontsize=9, 
                                            bbox=dict(facecolor="white", edgecolor="blue", boxstyle="round,pad=0.3"))
                option_prices_ax.annotate(f"Put: ${actual_put_y:.2f}", xy=(actual_put_x, actual_put_y), 
                                            xytext=(actual_put_x - 5, actual_put_y + 5),
                                            arrowprops=dict(facecolor='red', arrowstyle="->"), fontsize=9, 
                                            bbox=dict(facecolor="white", edgecolor="red", boxstyle="round,pad=0.3"))
                
                st.pyplot(option_prices_graph)
            
            with monte_carlo_graph_tab:
                monte_carlo_graph, monte_carlo_ax = plt.subplots(figsize=(10,5))
                
                for path in all_simulations:
                    rand_col = np.random.rand(3,)
                    monte_carlo_ax.plot(path, color=rand_col, alpha=0.5)
                
                avg_path = np.mean(all_simulations, axis=0)
                monte_carlo_ax.plot(avg_path, color='red', label='Average Path', linewidth=2)

                # Formatting
                monte_carlo_ax.set_xlim(0, time_to_expiry)
                monte_carlo_ax.set_title(f'Simulated Price Paths', fontsize=14, fontweight="bold")
                monte_carlo_ax.set_xlabel('Time Steps (days)', fontsize=12)
                monte_carlo_ax.set_ylabel('Price', fontsize=12)
                monte_carlo_ax.legend(loc="upper left", fontsize=12)
                monte_carlo_ax.grid(True, linestyle="--", alpha=0.7)

                monte_carlo_ax.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))

                st.pyplot(monte_carlo_graph)

        # Put this after everything on the main page has finished loading to finish status loaders
        result_loading_placeholder_status1.update(label="Results now completed!", state="complete", expanded=False)
        sleeper.sleep(1)
        result_loading_placeholder1.empty()
        calculation_loading_status.update(
            label="🧮 Model complete!", state="complete", expanded=False
        )
