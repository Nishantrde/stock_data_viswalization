import pandas as pd
from nsepython import nse_eq_symbols, equity_history
from datetime import date, timedelta


def get_companies_name():
    return nse_eq_symbols()


def get_stock_data(symbol, series="EQ", days=30):
    """
    Retrieves historical stock data for the last specified number of days and 
    adds daily return, volatility, average close, high, and low.

    Args:
        symbol (str): The stock symbol (e.g., "SBIN").
        series (str): The series type (e.g., "EQ" for equity).
        days (int): The number of days of historical data to retrieve.

    Returns:
        pandas.DataFrame: A DataFrame with the stock data and calculated metrics.
    """
    # Define date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    # Format dates
    start_date_str = start_date.strftime("%d-%m-%Y")
    end_date_str = end_date.strftime("%d-%m-%Y")

    # Fetch data using nsepython
    historical_data = equity_history(symbol, series, start_date_str, end_date_str)

    # Calculate Daily Return: (Close - Open) / Open
    historical_data['Daily Return'] = (historical_data['CH_CLOSING_PRICE'] - historical_data['CH_OPENING_PRICE']) / historical_data['CH_OPENING_PRICE']

    # Calculate Volatility Score: Standard Deviation of returns
    # For a rolling volatility, you would use `.rolling(window).std()`
    daily_returns = historical_data['CH_CLOSING_PRICE'].pct_change().dropna()
    historical_data['Volatility Score'] = daily_returns.rolling(window=len(daily_returns)).std()
    
    # Calculate Average Close, High, and Low for the period
    historical_data['Average Close'] = historical_data['CH_CLOSING_PRICE'].mean()
    historical_data['Average High'] = historical_data['CH_TRADE_HIGH_PRICE'].mean()
    historical_data['Average Low'] = historical_data['CH_TRADE_LOW_PRICE'].mean()

    return historical_data

# print(get_companies_name())

