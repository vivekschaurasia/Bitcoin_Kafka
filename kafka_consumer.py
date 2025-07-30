# kafka_consumer.py
import json
from confluent_kafka import Consumer
from threading import Thread
from datetime import datetime, timedelta

latest_row = {}
last_saved_minute = None

def start_kafka_listener():
    def loop():
        global latest_row, last_saved_minute

        c = Consumer({
            'bootstrap.servers': 'localhost:9092',
            'group.id': 'btc_fastapi_30min',
            'auto.offset.reset': 'latest'
        })
        c.subscribe(["btc_ohlc"])
        print("🕒 Kafka listener running (30-minute interval)")

        while True:
            msg = c.poll(1.0)
            if msg is None or msg.error():
                continue

            data = json.loads(msg.value().decode("utf-8"))
            timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")

            # First data or 30 min elapsed?
            if not last_saved_minute or (timestamp - last_saved_minute) >= timedelta(minutes=30):
                latest_row = data
                last_saved_minute = timestamp
                print(f"✅ New row saved for prediction: {latest_row['timestamp']}")

    Thread(target=loop, daemon=True).start()
