import time
import json
import requests
from datetime import datetime
from confluent_kafka import Producer

TOPIC = "btc_ohlc"
BOOTSTRAP_SERVERS = "localhost:9092"

p = Producer({'bootstrap.servers': BOOTSTRAP_SERVERS})

def fetch_current_ohlc():
    url = "https://api.binance.us/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "limit": 1
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()[0]

    return {
        "timestamp": datetime.fromtimestamp(data[0] / 1000).strftime("%Y-%m-%d %H:%M:%S"),
        "open": float(data[1]),
        "high": float(data[2]),
        "low": float(data[3]),
        "close": float(data[4])
    }

def delivery_report(err, msg):
    if err:
        print("Delivery failed:", err)
    else:
        print(f"Sent to {msg.topic()} @ offset {msg.offset()}")

while True:
    try:
        ohlc = fetch_current_ohlc()
        message = json.dumps(ohlc)
        p.produce(TOPIC, value=message, callback=delivery_report)
        p.flush()
    except Exception as e:
        print("Error:", e)

    # Wait 60 seconds
    time.sleep(60)
