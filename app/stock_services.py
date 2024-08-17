# Import standard libraries.
import requests


def get_info(ticker):
    """
    Returns information about a stock using AlphaVantage API.
    AlphaVantage API : https://www.alphavantage.co/

    Parameters
    ----------
    ticker : str
        The ticker of the stock.

    Returns
    -------
    data : dict
        Contains information about the stock, if the stock was found.

    dict
        Contains an error message, if the stock was not found.
    """

    url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={ticker}&apikey="
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if "Information" in data:
            return {"error": "API Limit Reached"}

        elif data:
            return data

        else:
            return {"error": "Stock Not Found"}

    return {"error": "API Error"}


def get_time_series(ticker):
    """
    Returns the 24-hour time-series of a stock using AlphaVantage API.
    AlphaVantage API : https://www.alphavantage.co/

    Parameters
    ----------
    ticker : str
        The ticker of the stock.

    Returns
    -------
    data : dict
        Contains information about the stock, if the stock was found.

    dict
        Contains an error message, if the stock was not found.
    """

    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey="
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        if "Information" in data:
            return {"error": "API Limit Reached"}

        elif "Error Message" in data:
            return {"error": "Stock Not Found"}

        else:
            return data["Time Series (Daily)"]

    return {"error": "API Error"}


def filter_info(data):
    """
    Returns the "needed" information of a stock.

    Parameters
    ----------
    data : dict
        Contains information about the stock, retrieved using the
        AlphaVantage API.

    Returns
    -------
    dict
        Contains the "needed" information about the stock.
    """

    keys = ["Symbol", "Name", "Exchange", "Currency", "Country", "Sector", "Industry", "Description"]
    return {k: data[k] for k in keys}


def filter_closing_prices(data):
    """
    Returns the closing prices of a stock.

    Parameters
    ----------
    data : dict
        Contains a time-series of the stock, retrieved using the
        AlphaVantage API.

    Returns
    -------
    dict
        Contains the time-series of closing-prices of the stock.
    """

    return {k: data[k]["4. close"] for k in data}


def filter_latest_quote(data):
    """
    Returns the latest quote of a stock.

    Parameters
    ----------
    data : dict
        Contains a time-series of the stock, retrieved using the
        AlphaVantage API.

    Returns
    -------
    quote : dict
        Contains the latest quote of the stock and the corresponding
        date.
    """

    quote = list(data.values())[0]
    quote["Date"] = next(iter(data))
    return quote
