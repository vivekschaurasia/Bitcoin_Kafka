import json
import joblib
import pandas as pd
from confluent_kafka import Consumer
from datetime import datetime

# Load trained models
model_open = joblib.load("model_open.pkl")
model_high = joblib.load("model_high.pkl")
model_low = joblib.load("model_low.pkl")
model_close = joblib.load("model_close.pkl")

# Set up Kafka consumer
c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'btc_ohlc_predictor',
    'auto.offset.reset': 'latest'
})
c.subscribe(["btc_ohlc"])

print("🔮 Kafka ML Consumer listening...")

# Track latest OHLC for lag
latest_row = None

try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Error:", msg.error())
            continue

        # Parse OHLC input
        data = json.loads(msg.value().decode("utf-8"))
        print("📥 Received:", data)

        # Prepare features using lag
        if latest_row:
            features = pd.DataFrame([{
                "open_lag1": latest_row["open"],
                "high_lag1": latest_row["high"],
                "low_lag1": latest_row["low"],
                "close_lag1": latest_row["close"]
            }])

            # Predict next OHLC
            pred_open = model_open.predict(features)[0]
            pred_high = model_high.predict(features)[0]
            pred_low = model_low.predict(features)[0]
            pred_close = model_close.predict(features)[0]

            print("🔮 Predicted Next OHLC:")
            print(f"Open:  {pred_open:.2f}")
            print(f"High:  {pred_high:.2f}")
            print(f"Low:   {pred_low:.2f}")
            print(f"Close: {pred_close:.2f}")

        # Update latest row
        latest_row = data

except KeyboardInterrupt:
    pass
finally:
    c.close()
