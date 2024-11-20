import sqlite3
import pandas as pd
from ta.momentum import RSIIndicator
from ta.volatility import BollingerBands
from ta.trend import EMAIndicator
from ta.volatility import AverageTrueRange
from ta.trend import MACD

# Connect to the SQLite database
db_path = "trading_data.db"
conn = sqlite3.connect(db_path)

# Fetch all table names
query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql(query, conn)
table_names = tables["name"].tolist()

# Function to calculate indicators
def calculate_indicators(data):
    # Initialize indicators
    data["RSI_6"] = RSIIndicator(close=data["close"], window=6).rsi()
    bollinger = BollingerBands(close=data["close"], window=10, window_dev=1.5)
    data["Bollinger_High"] = bollinger.bollinger_hband()
    data["Bollinger_Low"] = bollinger.bollinger_lband()
    data["EMA_5"] = EMAIndicator(close=data["close"], window=5).ema_indicator()
    data["EMA_20"] = EMAIndicator(close=data["close"], window=20).ema_indicator()
    atr = AverageTrueRange(high=data["high"], low=data["low"], close=data["close"], window=3)
    data["ATR_3"] = atr.average_true_range()
    macd = MACD(close=data["close"], window_slow=19, window_fast=6, window_sign=3)
    data["MACD"] = macd.macd()
    data["MACD_Signal"] = macd.macd_signal()
    data["MACD_Diff"] = macd.macd_diff()
    return data

# Process each table
for table in table_names:
    # Load data
    query = f"SELECT * FROM {table};"
    data = pd.read_sql(query, conn)
    
    # Ensure correct data types and sorting
    data = data.sort_values(by="timestamp")
    data = data.dropna(subset=["close", "high", "low", "open", "volume"])
    
    # Calculate indicators
    try:
        data = calculate_indicators(data)
    except Exception as e:
        print(f"Error processing table {table}: {e}")
        continue
    
    # Write back to the database
    data.to_sql(table, conn, if_exists="replace", index=False)

# Close the connection
conn.close()

"Indicators calculated and stored for all tables."
