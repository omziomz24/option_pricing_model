from .utils import pd, Prophet
from .constants import rfr_datasets_mapping

class RFR_Projection:

    def __init__(self, proj_period):
        self.proj_period = proj_period
        self.projected_df = None

    def forecast(self, data: str, available_data: dict = rfr_datasets_mapping):
        
        # Read and clean data
        df = pd.read_csv('data/' + available_data.get(data[:-2]), parse_dates=['ds'], dayfirst=True)
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
