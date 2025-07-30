"""import requests
import pandas as pd
from datetime import datetime

def fetch_binance_ohlc_1min():
    url = "https://api.binance.us/api/v3/klines"

    params = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "limit": 60  # Last 60 minutes
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()

    # Create DataFrame
    df = pd.DataFrame(data, columns=[
        "open_time", "open", "high", "low", "close",
        "volume", "close_time", "quote_asset_volume",
        "number_of_trades", "taker_buy_base_volume",
        "taker_buy_quote_volume", "ignore"
    ])

    # Process
    df["timestamp"] = pd.to_datetime(df["open_time"], unit="ms").dt.strftime("%H:%M")
    df = df[["timestamp", "high", "low", "open", "close"]]
    df = df.astype({"open": float, "high": float, "low": float, "close": float})
    
    return df

# Fetch and display

df = fetch_binance_ohlc_1min()
df.to_csv("btc_ohlc_last_hour.csv", index=False)
print("Saved to btc_ohlc_last_hour.csv")

"""


import requests
import pandas as pd
from datetime import datetime

def get_current_ohlc():
    url = "https://api.binance.us/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "limit": 1  # Get only the most recent 1-minute candle
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()[0]

    ohlc = {
        "timestamp": datetime.fromtimestamp(data[0] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
        "open": float(data[1]),
        "high": float(data[2]),
        "low": float(data[3]),
        "close": float(data[4])
    }

    return ohlc

# Example usage
current_ohlc = get_current_ohlc()
print("Current 1-min OHLC:")
print(current_ohlc)
