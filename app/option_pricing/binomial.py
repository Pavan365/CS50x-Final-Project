# Import external libraries.
import numpy as np

class BinomialCRR:
    """
    Represents the Binomial-CRR model for option pricing.

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
        Contstructs a BinomialCRR object.

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
        Calculates the price of the option using the Binomial-CRR model.

        Parameters
        ----------
        type : str, options = [call, put]
            The type of the option.

        Returns
        -------
        float
            The price of the option.
        """

        n = 25000
        dt = self.time / n

        u = np.exp(self.sigma * np.sqrt(dt))
        d = np.exp(-self.sigma * np.sqrt(dt))
        p = (np.exp(self.rfr * dt) - d) / (u - d)

        asset_prices = self.spot * (u ** np.arange(0, n+1, 1)) * (d ** np.arange(n, -1, -1))

        if type == "call":
            option_values = np.maximum(asset_prices - self.strike, 0)

        elif type == "put":
            option_values = np.maximum(self.strike - asset_prices, 0)

        for i in range(n, 0, -1):
            option_values = np.exp(-self.rfr * dt) * ((p * option_values[1:i+1]) + ((1 - p) * option_values[0:i]))

        return option_values[0]

