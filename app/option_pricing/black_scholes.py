# Import external libraries.
import numpy as np
from scipy.stats import norm

class BlackScholes():
    """
    Represents the Black-Scholes model for option pricing.

    Attributes
    ----------
    spot   : float
        The spot price of the asset.
    strike : float
        The strike price of the asset.
    time   : float
        The time till expiration of the option, in years.
    rfr    : float
        The risk free rate of the asset.
    sigma  : float
        The volatility of the asset.
    """

    def __init__(self, spot, strike, time, rfr, sigma):
        """
        Contstructs a BlackScholes object.

        Parameters
        ----------
        spot   : float
            The spot price of the asset.
        strike : float
            The strike price of the asset.
        time   : float
            The time till expiration of the option.
        rfr    : float
            The risk free rate of the asset.
        sigma  : float
            The volatility of the asset.
        """

        self.spot = spot
        self.strike = strike
        self.time = time
        self.rfr = rfr
        self.sigma = sigma

    @staticmethod
    def normal(x):
        """ Returns the normal cumulative distribution function. """
        return norm.cdf(x)

    def price(self, type):
        """
        Calculates the price of the option using the Black-Scholes
        model.

        Parameters
        ----------
        type : str, options = [call, put]
            The type of the option.

        Returns
        -------
        float
            The price of the option.
        """

        d1 = (np.log(self.spot / self.strike) + ((self.rfr + ((self.sigma ** 2) / 2)) * self.time)) / (self.sigma * np.sqrt(self.time))
        d2 = d1 - (self.sigma * np.sqrt(self.time))

        if type == "call":
            return (self.spot * self.normal(d1)) - (self.normal(d2) * self.strike * np.exp(-(self.rfr * self.time)))

        elif type == "put":
            return (self.normal(-d2) * self.strike * np.exp(-(self.rfr * self.time))) - (self.spot * self.normal(-d1))

