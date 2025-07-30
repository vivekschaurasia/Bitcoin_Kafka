# cd C:\kafka_2.13-3.9.0
#for run  .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties
#for run  .\bin\windows\kafka-server-start.bat .\config\server.properties
#then run  .\bin\windows\kafka-topics.bat --create --topic btc_ohlc --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
#then run conumer.py and producer.py

import json
import os
import pandas as pd
from confluent_kafka import Consumer
from datetime import datetime

TOPIC = "btc_ohlc"
CSV_FILE = "btc_ohlc_data.csv"

# Load existing data if file exists
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close"])

c = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'btc_ohlc_group',
    'auto.offset.reset': 'earliest'
})
c.subscribe([TOPIC])

print("Consumer listening...")
from datetime import datetime, timedelta

buffer = []
next_write_time = datetime.now() + timedelta(minutes=30)
try:
    while True:
        msg = c.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error:", msg.error())
            continue

        data = json.loads(msg.value().decode("utf-8"))
        buffer.append(data)

        if datetime.now() >= next_write_time:
            print(f"Writing {len(buffer)} rows to CSV at {datetime.now()}")
            df = pd.DataFrame(buffer)
            if os.path.exists(CSV_FILE):
                existing_df = pd.read_csv(CSV_FILE)
                df = pd.concat([existing_df, df], ignore_index=True)
            df.to_csv(CSV_FILE, index=False)
            buffer = []
            next_write_time = datetime.now() + timedelta(minutes=30)

except KeyboardInterrupt:
    pass
finally:
    c.close()
