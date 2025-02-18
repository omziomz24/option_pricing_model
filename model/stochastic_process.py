from .utils import np, math

class Stochastic_Process:
    """Implements various stochastic processes including ABM, GBM, and MMAR."""

    def __init__(self, type: str, initial_price: float, drift: float, delta_t: float, volatility: float, hurst: float = 0.7, cascade_depth: int = 8, steps: int = 252):
        """
        :param type: Type of stochastic process ("Arithmetic Brownian Motion", "Geometric Brownian Motion", "Multifractal Model of Asset Returns")
        :param initial_price: Initial price of the asset
        :param drift: Drift parameter (mu)
        :param delta_t: Time step size
        :param volatility: Volatility parameter (sigma)
        :param hurst: Hurst exponent (only for MMAR)
        :param cascade_depth: Number of iterations in the multifractal cascade
        :param steps: Number of time steps (for MMAR)
        """
        self.type  = type
        self.drift = drift
        self.volatility = volatility
        self.delta_t = delta_t
        self.current_price = initial_price
        self.prices = [initial_price]
        self.hurst = hurst  # Only used in MMAR
        self.cascade_depth = cascade_depth  # Depth of the multifractal cascade
        self.steps = steps  # Number of simulation steps

    def time_step(self):
        """Simulates one time step for the stochastic process."""

        # **Arithmetic Brownian Motion (ABM)**
        if self.type.upper() == "Arithmetic Brownian Motion".upper(): 
            dW = np.random.normal(0, math.sqrt(self.delta_t))
            dS = self.drift * self.delta_t + self.volatility * dW
            self.current_price += dS
            self.prices.append(self.current_price)

        # **Geometric Brownian Motion (GBM)**
        elif self.type.upper() == "Geometric Brownian Motion".upper():
            dW = np.random.normal(0, math.sqrt(self.delta_t))
            dS = self.current_price * np.exp(
                (self.drift - 0.5 * self.volatility**2) * self.delta_t + self.volatility * dW
            ) - self.current_price
            self.current_price += dS
            self.prices.append(self.current_price)

        # **Multifractal Model of Asset Returns (MMAR)**
        elif self.type.upper() == "Multifractal Model of Asset Returns".upper():
            # Simulate MMAR over multiple steps
            self.prices = self.simulate_mmar()
            self.current_price = self.prices[-1]  # Update current price

    def generate_multifractal_time(self):
        """
        Generate a binomial multiplicative cascade for time deformation.
        The cascade assigns random "market activity rates" to each time step.
        """
        weights = np.ones(self.steps)

        for _ in range(self.cascade_depth):
            rand_split = np.random.uniform(0.2, 0.8, self.steps)
            weights *= np.where(np.random.rand(self.steps) < 0.5, rand_split, 1 - rand_split)

        # Normalize and ensure strictly increasing time
        multifractal_time = np.cumsum(weights / np.sum(weights)) * self.steps * self.delta_t
        multifractal_time = np.maximum.accumulate(multifractal_time)
        
        return multifractal_time

    def simulate_mmar(self):
        """
        Simulates MMAR using a GBM base model and multifractal time deformation.
        """
        # Generate GBM log-returns
        normal_shocks = np.random.normal(0, np.sqrt(self.delta_t), self.steps)
        returns = (self.drift - 0.5 * self.volatility**2) * self.delta_t + self.volatility * normal_shocks

        # Generate multifractal time
        fractal_time = self.generate_multifractal_time()

        # Apply time deformation: Interpolate GBM returns using multifractal time
        time_deformed_returns = np.interp(np.arange(self.steps) * self.delta_t, fractal_time, returns)

        # Compute log-price path (start at log(S0))
        log_prices = np.cumsum(time_deformed_returns)
        log_prices = log_prices - log_prices[0] + np.log(self.prices[0])

        # Convert back to normal price scale
        return np.exp(log_prices)
