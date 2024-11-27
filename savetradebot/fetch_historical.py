import ccxt
import pandas as pd
from datetime import datetime

# Binance-API Verbindung
exchange = ccxt.binance()

def fetch_historical_data(pair, timeframe='1m', limit=500):
    """
    Historische OHLCV-Daten für ein Handelspaar abrufen.
    """
    try:
        ohlcv = exchange.fetch_ohlcv(pair, timeframe=timeframe, limit=limit)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        
        # Zeitstempel in ein lesbares Format konvertieren
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        
        return df
    except Exception as e:
        print(f"Fehler beim Abrufen historischer Daten für {pair}: {e}")
        return None

if __name__ == "__main__":
    # Beispiel: BTC/USDT
    pair = 'BTC/USDT'
    data = fetch_historical_data(pair)
    if data is not None:
        print(f"Daten für {pair}:\n{data.head()}")
