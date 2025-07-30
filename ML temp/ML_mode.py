import pandas as pd
from datetime import timedelta
from xgboost import XGBRegressor

# Step 1: Load the dataset
df = pd.read_csv("df_after_fe.csv")
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values('Date').reset_index(drop=True)

# Step 2: Feature Engineering - Create lag features
LAG_DAYS = 5
for lag in range(1, LAG_DAYS + 1):
    for col in ['Open', 'High', 'Low', 'Close']:
        df[f'{col}_lag_{lag}'] = df[col].shift(lag)

df = df.dropna().reset_index(drop=True)

# Step 3: Prepare training data
features = [col for col in df.columns if 'lag' in col]
targets = ['Open', 'High', 'Low', 'Close']

train_df = df.iloc[:-30]
X_train = train_df[features]
y_train = train_df[targets]

# Step 4: Train one model per target using XGBoost
models = {}
for target in targets:
    model = XGBRegressor(n_estimators=30, max_depth=3, random_state=42)
    model.fit(X_train, y_train[target])
    models[target] = model

# Step 5: Recursive prediction for next 30 days
last_known = df.iloc[-LAG_DAYS:].copy()
predictions = {key: [] for key in targets}

for i in range(30):
    row = {}
    for lag in range(1, LAG_DAYS + 1):
        for col in targets:
            row[f'{col}_lag_{lag}'] = last_known.iloc[-lag][col]
    X_pred = pd.DataFrame([row])
    
    pred = {target: models[target].predict(X_pred)[0] for target in targets}
    for key in targets:
        predictions[key].append(pred[key])

    next_date = last_known.iloc[-1]['Date'] + timedelta(days=1)
    new_row = {
        'Date': next_date,
        'Open': pred['Open'],
        'High': pred['High'],
        'Low': pred['Low'],
        'Close': pred['Close'],
        'Volume': 0,
        'year': next_date.year,
        'month': next_date.month,
        'day': next_date.day
    }
    last_known = pd.concat([last_known, pd.DataFrame([new_row])], ignore_index=True)

# Step 6: Create output DataFrame
future_dates = pd.date_range(start=df['Date'].iloc[-1] + timedelta(days=1), periods=30)
pred_df = pd.DataFrame({
    'Date': future_dates,
    'Open': predictions['Open'],
    'High': predictions['High'],
    'Low': predictions['Low'],
    'Close': predictions['Close']
})


# Step 7: Save or visualize
pred_df.to_csv("predicted_ohlc_30_days.csv", index=False)
print("Prediction complete. Results saved to predicted_ohlc_30_days.csv.")


print("Done")