import os
import sqlite3
from binance.client import Client
from datetime import datetime
import pandas as pd

# Load API keys from environment variables
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

if not API_KEY or not API_SECRET:
    raise ValueError("API keys are not set. Please check your environment variables.")

# Initialize Binance client
client = Client(API_KEY, API_SECRET, testnet=True)

# SQLite database setup
DB_PATH = "trading_data.db"

def create_database():
    """Create SQLite database and tables if not already exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS historical_data (
            pair TEXT,
            timestamp INTEGER,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            PRIMARY KEY (pair, timestamp)
        )
    """)
    conn.commit()
    conn.close()

def fetch_historical_data(pair, interval="1h", start_str="1 month ago UTC"):
    """
    Fetch historical candlestick data for a given pair and store it in SQLite.
    
    Args:
        pair (str): Trading pair (e.g., BTCUSDT).
        interval (str): Binance Kline interval (e.g., '1h', '1d').
        start_str (str): Start time for historical data (e.g., '1 month ago UTC').
    """
    try:
        print(f"Fetching historical data for {pair}...")
        klines = client.get_historical_klines(pair, interval, start_str)
        
        # Format data into a Pandas DataFrame
        columns = ["timestamp", "open", "high", "low", "close", "volume", "close_time",
                   "quote_asset_volume", "number_of_trades", "taker_buy_base", "taker_buy_quote", "ignore"]
        df = pd.DataFrame(klines, columns=columns)
        df = df[["timestamp", "open", "high", "low", "close", "volume"]]
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        
        # Save to SQLite
        conn = sqlite3.connect(DB_PATH)
        df.to_sql("historical_data", conn, if_exists="append", index=False)
        conn.close()
        print(f"Data for {pair} saved successfully.")
    except Exception as e:
        print(f"Error fetching data for {pair}: {e}")

def main():
    create_database()
    trading_pairs = ["BTCUSDT", "ETHUSDT"]  # Add more pairs as needed
    for pair in trading_pairs:
        fetch_historical_data(pair)

if __name__ == "__main__":
    main()
