import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

class ML_Volatility_Model:
    def __init__(self, ticker, start, end):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.model = LinearRegression()  # Use Linear Regression instead of Random Forest

    def prepare_features(self, data):
        """Create feature set"""
        # Ensure "Log Return" exists before using it
        if "Log Return" not in data.columns:
            data["Log Return"] = np.log(data["Close"] / data["Close"].shift(1))

        # Short-term returns
        data["Return_1D"] = data["Log Return"].shift(1)  # 1-day return
        data["Return_5D"] = data["Log Return"].rolling(window=5).mean().shift(1)  # 1-week return
        data["Return_20D"] = data["Log Return"].rolling(window=20).mean().shift(1)  # 1-month return
        
        # Longer-term returns
        data["Return_63D"] = data["Log Return"].rolling(window=63).mean().shift(1)  # 3-month return
        data["Return_126D"] = data["Log Return"].rolling(window=126).mean().shift(1)  # 6-month return

        # Feature selection
        feature_cols = ["Return_1D", "Return_5D", "Return_20D", "Return_63D", "Return_126D"]

        # Drop rows with missing values (NaNs)
        data = data[feature_cols + ["Volatility"]].dropna()

        return data

    def train_model(self, data):
        """Train ML model to predict volatility"""
        # Store data for later use in predictions
        self.recent_stock_data = data

        # Compute "Log Return" and "Volatility" before calling prepare_features()
        data["Log Return"] = np.log(data["Close"] / data["Close"].shift(1))
        data["Volatility"] = data["Log Return"].rolling(window=20).std() * np.sqrt(252)

        # Drop NaN values
        data = data.dropna()

        # Now, prepare the feature set
        data = self.prepare_features(data)

        # Train the model
        X = data.drop(columns=["Volatility"])
        y = data["Volatility"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        self.model.fit(X_train, y_train)
        predictions = self.model.predict(X_test)

<<<<<<< HEAD
        # error = mean_squared_error(y_test, predictions, squared=False)
        # print(f"Root Mean Squared Error of Machine Learning Volatility Model: {error:.3f}")
=======
        #error = mean_squared_error(y_test, predictions, squared=False)
        #print(f"Root Mean Squared Error of Machine Learning Volatility Model: {error:.3f}")
>>>>>>> 5bd147f94 (Updated existing files)


    def predict_volatility(self):
        """Predict future volatility using trained ML model"""
        recent_data = self.recent_stock_data
        recent_features = self.prepare_features(recent_data).drop(columns=["Volatility"])
        sigma_ml = self.model.predict(recent_features.tail(1))[0]

        # Fetch historical volatility
        sigma_hist = np.std(recent_data["Log Return"].dropna()) * np.sqrt(252)

        # Blend ML and historical volatility to smooth prediction
        final_volatility = (sigma_ml + sigma_hist) / 2

        return final_volatility
