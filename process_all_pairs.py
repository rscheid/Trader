import ccxt
import sqlite3
import pandas as pd
from multiprocessing import Pool
from datetime import datetime

# Binance-API Verbindung
exchange = ccxt.binance()

def fetch_trading_pairs():
    """
    Handelspaare von Binance abrufen.
    """
    markets = exchange.load_markets()
    return [market for market in markets]


import time

def fetch_historical_data(pair, timeframe='1m', limit=500, retries=3):
    """
    Historische OHLCV-Daten für ein Handelspaar abrufen, mit Fehlerhandling.
    """
    for attempt in range(retries):
        try:
            ohlcv = exchange.fetch_ohlcv(pair, timeframe=timeframe, limit=limit)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            return df
        except Exception as e:
            print(f"Fehler beim Abrufen der Daten für {pair}: {e}")
            if attempt < retries - 1:
                print(f"Erneuter Versuch für {pair} in 5 Sekunden...")
                time.sleep(5)  # Wartezeit vor erneutem Versuch
            else:
                print(f"Maximale Versuche für {pair} erreicht. Überspringe.")
                return None


def calculate_fees(df, fee_rate=0.001):
    """
    Gebühren berechnen und Daten erweitern.
    """
    df['fees'] = df['close'] * df['volume'] * fee_rate
    df['net_volume'] = df['volume'] - df['fees']
    return df

def store_to_sqlite(df, table_name, db_name='trading_data.db'):
    """
    Speichert die Daten in einer SQLite-Datenbank.
    """
    try:
        conn = sqlite3.connect(db_name)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        print(f"Daten für {table_name} erfolgreich gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Daten in {table_name}: {e}")

def process_pair(pair):
    """
    Verarbeitet ein einzelnes Handelspaar: Abrufen, Gebühren berechnen, Speichern.
    """
    print(f"Verarbeite {pair}...")
    data = fetch_historical_data(pair)
    if data is not None:
        data = calculate_fees(data)  # Gebühren berechnen
        table_name = pair.replace('/', '_')
        store_to_sqlite(data, table_name)

if __name__ == "__main__":
    # 1. Handelspaare abrufen
    trading_pairs = fetch_trading_pairs()
    print(f"Gefundene Handelspaare: {len(trading_pairs)}")

    # 2. Multiprocessing für die Verarbeitung
    with Pool(processes=10) as pool:  # Passe die Anzahl der Prozesse an deinen Server an
        pool.map(process_pair, trading_pairs[:50])  # Begrenzung zum Testen auf die ersten 50 Paare
