from .utils import pd, Prophet

class RFR_Projection:

    def __init__(self, proj_period):
        self.proj_period = proj_period
        self.projected_df = None

    def forecast(self, data: str):
        available_data = {
            "AU-10": 'AUS_10yr_rfr.csv',
            "AU-5": 'AUS_5yr_rfr.csv',
            "AU-3": 'AUS_3yr_rfr.csv',
            "AU-2": 'AUS_2yr_rfr.csv',
            "US-10": 'US_10yr_rfr.csv',
            "US-5": 'US_5yr_rfr.csv',
            "US-2": 'US_2yr_rfr.csv',
            "US-1": 'US_1yr_rfr.csv'
        }
        
        # Read and clean data
        df = pd.read_csv('data/' + available_data.get(data), parse_dates=['ds'], dayfirst=True)
        df = df[df['y'] != 0]

        # Set a pessimistic cap for logistic growth.
        # For example, if your rates are expressed in decimals (e.g., 0.03 for 3%),
        # and you want to force a ceiling of 6%, then set cap = 0.06.
        df['cap'] = 0.06

        # Initialize Prophet with logistic growth and a lower changepoint prior scale
        m = Prophet(growth='logistic', changepoint_prior_scale=0.01)
        m.fit(df)
    
        # Create a dataframe for the forecast period
        future = m.make_future_dataframe(periods=self.proj_period)
        # When using logistic growth, add the cap to the future frame.
        future['cap'] = 0.06
        
        forecast = m.predict(future)
        
        self.projected_df = forecast[['ds', 'yhat']]
        self.projected_df.rename(columns={'ds': 'Date', 'yhat': 'Rate'}, inplace=True)
    
    def get_forecast(self):
        return self.projected_df
