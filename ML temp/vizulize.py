import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("df_after_fe.csv")
df['Date'] = pd.to_datetime(df['Date'])
actual_df = df.sort_values('Date').iloc[-30:].copy()

pred_df = pd.read_csv("predicted_ohlc_30_days.csv")
pred_df['Date'] = pd.to_datetime(pred_df['Date'])

# Add a flag to track which is which
actual_df['Type'] = 'Actual'
pred_df['Type'] = 'Predicted'

# Match columns and combine
merged_df = pd.concat([actual_df[['Date', 'Open', 'High', 'Low', 'Close', 'Type']],
                       pred_df[['Date', 'Open', 'High', 'Low', 'Close']].assign(Type='Predicted')],
                      ignore_index=True)

# Plot each OHLC value
for col in ['Open', 'High', 'Low', 'Close']:
    plt.figure(figsize=(12, 5))
    actual = merged_df[merged_df['Type'] == 'Actual']
    predicted = merged_df[merged_df['Type'] == 'Predicted']
    
    # Plot full timeline
    plt.plot(actual['Date'], actual[col], label='Actual', marker='o')
    plt.plot(predicted['Date'], predicted[col], label='Predicted', marker='s')
    
    plt.title(f"{col} Price (Actual Last 30 Days + Predicted Next 30 Days)")
    plt.xlabel("Date")
    plt.ylabel(f"{col} Price")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
