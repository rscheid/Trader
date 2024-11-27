import os
import pandas as pd
from binance.client import Client
from config import API_KEY, API_SECRET, TESTNET, DATA_PATH

# Binance-Client initialisieren
client = Client(API_KEY, API_SECRET, testnet=TESTNET)

def fetch_historical_data(symbol, interval, start_date):
    """
    Lädt historische Marktdaten von Binance.
    
    :param symbol: Das Handelspaar, z. B. "BTCUSDT".
    :param interval: Der Zeitrahmen, z. B. Client.KLINE_INTERVAL_1HOUR.
    :param start_date: Das Startdatum, z. B. "1 Jan, 2023".
    :return: DataFrame mit historischen Daten.
    """
    klines = client.get_historical_klines(symbol, interval, start_date)
    data = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])
    # Zeitstempel in lesbares Format konvertieren
    data["timestamp"] = pd.to_datetime(data["timestamp"], unit="ms")
    return data[["timestamp", "open", "high", "low", "close", "volume"]]

def save_data(data, symbol):
    """
    Speichert die Daten lokal als CSV-Datei.
    
    :param data: Der DataFrame mit den Daten.
    :param symbol: Das Handelspaar, z. B. "BTCUSDT".
    """
    os.makedirs(DATA_PATH, exist_ok=True)
    file_path = os.path.join(DATA_PATH, f"{symbol}.csv")
    data.to_csv(file_path, index=False)
    print(f"Daten für {symbol} gespeichert unter: {file_path}")

if __name__ == "__main__":
    # Beispiel: Historische Daten für BTC/USDT abrufen
    symbol = "BTCUSDT"
    interval = Client.KLINE_INTERVAL_1HOUR
    start_date = "1 Jan, 2023"

    print(f"Historische Daten für {symbol} werden abgerufen...")
    data = fetch_historical_data(symbol, interval, start_date)
    save_data(data, symbol)
    print(f"{symbol} - Daten erfolgreich geladen und gespeichert.")
