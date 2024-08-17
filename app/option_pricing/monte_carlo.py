# Import external libraries.
import numpy as np

class MonteCarlo:
    """
    Represents the Monte-Carlo model for option pricing.

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
        Contstructs a MonteCarlo object.

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

    def price(self, type):
        """
        Calculates the price of the option using the Monte-Carlo model.

        Parameters
        ----------
        type : str, options = [call, put]
            The type of the option.

        Returns
        -------
        float
            The price of the option.
        """

        sims = 1000000
        
        z = np.random.standard_normal(sims)
        drift = (self.rfr - (0.5 * (self.sigma ** 2))) * self.time

        asset_prices = self.spot * np.exp(drift + (self.sigma * np.sqrt(self.time) * z))

        if type == "call":
            option_values = np.maximum(asset_prices - self.strike, 0)

        elif type == "put":
            option_values = np.maximum(self.strike - asset_prices, 0)

        option_price = np.exp(-self.rfr * self.time) * np.mean(option_values)

        return option_price
