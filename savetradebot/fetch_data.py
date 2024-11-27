import ccxt
import pandas as pd
from dotenv import load_dotenv
import os

# .env-Datei laden
load_dotenv()

# Binance-API-Schlüssel aus Umgebungsvariablen lesen
API_KEY = os.getenv("TESTNET_API_KEY")
SECRET_KEY = os.getenv("TESTNET_SECRET")

# Verbindung zur Binance-Testnet-API herstellen
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
})

# Testnet-Modus aktivieren
exchange.set_sandbox_mode(True)

# Symbol und Zeitrahmen
symbol = "BTC/USDT"
timeframe = "1m"  # 1-Minuten-Daten
limit = 1000      # Maximal verfügbare Daten (Binance-Limit)

# Daten abrufen
print("Fetching historical data...")
ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)

# In ein Pandas DataFrame umwandeln
df = pd.DataFrame(ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"])
df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")  # Zeitstempel formatieren

# CSV speichern
output_file = "historical_data.csv"
df.to_csv(output_file, index=False)
print(f"Data saved to {output_file}")
