import pandas as pd
from nsepython import nse_eq_symbols, equity_history
from datetime import date, timedelta


def get_companies_name():
    return nse_eq_symbols()


def get_stock_data(symbol, series="EQ", days=30):
    end_date = date.today()
    start_date = end_date - timedelta(days=days)

    start_date_str = start_date.strftime("%d-%m-%Y")
    end_date_str = end_date.strftime("%d-%m-%Y")

    historical_data = equity_history(symbol, series, start_date_str, end_date_str)
    df = pd.DataFrame(historical_data)

    # Convert numeric columns
    df["CH_OPENING_PRICE"] = pd.to_numeric(df["CH_OPENING_PRICE"], errors="coerce")
    df["CH_CLOSING_PRICE"] = pd.to_numeric(df["CH_CLOSING_PRICE"], errors="coerce")
    df["CH_TRADE_HIGH_PRICE"] = pd.to_numeric(df["CH_TRADE_HIGH_PRICE"], errors="coerce")
    df["CH_TRADE_LOW_PRICE"] = pd.to_numeric(df["CH_TRADE_LOW_PRICE"], errors="coerce")
    df.dropna(subset=["CH_CLOSING_PRICE", "CH_OPENING_PRICE"], inplace=True)

    # Date conversion
    df["DATE"] = pd.to_datetime(df["CH_TIMESTAMP"])
    df.sort_values("DATE", inplace=True)

    # === 📈 Core Calculations ===
    # Daily Return
    df["DAILY_RETURN"] = (df["CH_CLOSING_PRICE"] - df["CH_OPENING_PRICE"]) / df["CH_OPENING_PRICE"]

    # 7-Day Moving Average
    df["MA7"] = df["CH_CLOSING_PRICE"].rolling(window=7).mean()

    # Volatility (std of returns)
    volatility = round(df["DAILY_RETURN"].std() * 100, 2)

    # Summary
    high_52 = df["CH_TRADE_HIGH_PRICE"].max()
    low_52 = df["CH_TRADE_LOW_PRICE"].min()
    avg_close = round(df["CH_CLOSING_PRICE"].mean(), 2)
    yearly_return = round(((df["CH_CLOSING_PRICE"].iloc[-1] - df["CH_CLOSING_PRICE"].iloc[0]) /
                           df["CH_CLOSING_PRICE"].iloc[0]) * 100, 2)
    avg_daily_return = round(df["DAILY_RETURN"].mean() * 100, 2)

    # Prepare for charts
    dates = df["DATE"].dt.strftime("%d-%b").tolist()
    close_prices = df["CH_CLOSING_PRICE"].tolist()
    daily_returns = (df["DAILY_RETURN"] * 100).tolist()
    ma7 = df["MA7"].tolist()

    return {
        "symbol": symbol,
        "high_52": float(high_52),
        "low_52": float(low_52),
        "avg_close": float(avg_close),
        "yearly_return": float(yearly_return),
        "avg_daily_return": float(avg_daily_return),
        "volatility": float(volatility),
        "dates": dates,
        "close_prices": close_prices,
        "daily_returns": daily_returns,
        "ma7": ma7
    }


# print(get_companies_name())

