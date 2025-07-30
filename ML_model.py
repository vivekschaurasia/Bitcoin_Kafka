import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Load and preprocess data
df = pd.read_csv("btc_ohlc_data.csv", parse_dates=["timestamp"])

# Create lag features
for col in ["open", "high", "low", "close"]:
    df[f"{col}_lag1"] = df[col].shift(1)

# Drop rows with NaNs from lagging
df = df.dropna().reset_index(drop=True)

# Features and Targets
feature_cols = ["open_lag1", "high_lag1", "low_lag1", "close_lag1"]

X = df[feature_cols]
y_open = df["open"]
y_high = df["high"]
y_low = df["low"]
y_close = df["close"]

# Train-test split (no shuffle since it's time-series)
X_train, X_test, y_open_train, y_open_test = train_test_split(X, y_open, test_size=0.2, shuffle=False)
_, _, y_high_train, y_high_test = train_test_split(X, y_high, test_size=0.2, shuffle=False)
_, _, y_low_train, y_low_test = train_test_split(X, y_low, test_size=0.2, shuffle=False)
_, _, y_close_train, y_close_test = train_test_split(X, y_close, test_size=0.2, shuffle=False)

# Train models
model_open = XGBRegressor().fit(X_train, y_open_train)
model_high = XGBRegressor().fit(X_train, y_high_train)
model_low = XGBRegressor().fit(X_train, y_low_train)
model_close = XGBRegressor().fit(X_train, y_close_train)

# Evaluate (optional)
for label, model, y_test, pred in zip(
    ["Open", "High", "Low", "Close"],
    [model_open, model_high, model_low, model_close],
    [y_open_test, y_high_test, y_low_test, y_close_test],
    [model_open.predict(X_test), model_high.predict(X_test),
     model_low.predict(X_test), model_close.predict(X_test)]
):
    print(f"{label} MSE: {mean_squared_error(y_test, pred):.2f}")

# Predict next OHLC from latest row
latest_features = df[feature_cols].iloc[[-1]]
next_open = model_open.predict(latest_features)[0]
next_high = model_high.predict(latest_features)[0]
next_low = model_low.predict(latest_features)[0]
next_close = model_close.predict(latest_features)[0]

#print("\n📈 Predicted Next OHLC:")
#print(f"Open:  {next_open:.2f}")
#print(f"High:  {next_high:.2f}")
#print(f"Low:   {next_low:.2f}")
#print(f"Close: {next_close:.2f}")


import joblib
# Save models
joblib.dump(model_open, "model_open.pkl")
joblib.dump(model_high, "model_high.pkl")
joblib.dump(model_low, "model_low.pkl")
joblib.dump(model_close, "model_close.pkl")