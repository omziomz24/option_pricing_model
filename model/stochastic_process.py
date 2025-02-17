from .utils import np, math

class Stochastic_Process: # Arithmetic Brownian Motion

    def __init__(self,  type: str, initial_price: float, drift: float, delta_t: float, volatility: float):
        self.type  = type
        self.drift = drift
        self.volatility = volatility
        self.delta_t = delta_t
        self.current_price = initial_price
        self.prices = [initial_price]

    def time_step(self):
        
        # Arithmetic Brownian Motion
        if self.type.upper() == "ABM": 
            # dS = mu*dt + sigma*dW
            # No compounding effect as does not use last price
            dW = np.random.normal(0, math.sqrt(self.delta_t))
            dS = self.drift * self.delta_t + self.volatility * dW

            # add to prices and update price with dS
            self.prices.append(self.current_price + dS)
            self.current_price += dS

        # Geometric Brownian Motion
        elif self.type.upper() == "GBM":
            # dS = S_t*mu*dt + S_t*sigma*dW
            # Has compounding effect as uses past price
            dW = np.random.normal(0, math.sqrt(self.delta_t))
            dS = self.current_price * np.exp(
                (self.drift - 0.5 * self.volatility**2) * self.delta_t + self.volatility * dW
            ) - self.current_price

            # add to prices and update price with dS
            self.prices.append(self.current_price + dS)
            self.current_price += dS
