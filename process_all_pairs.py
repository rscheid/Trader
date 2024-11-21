import logging
import time
import sqlite3
from database import load_active_pairs, log_to_db
from trading_logic import setup_exchange, calculate_rsi
from dotenv import load_dotenv
import os
import ccxt

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Binance-Setup
load_dotenv()
API_KEY = os.getenv("TESTNET_API_KEY")
SECRET_KEY = os.getenv("TESTNET_SECRET")

if not API_KEY or not SECRET_KEY:
    raise ValueError("API_KEY und SECRET_KEY müssen in der .env-Datei definiert sein!")

exchange = setup_exchange(API_KEY, SECRET_KEY)

def fetch_candle_data(symbol, timeframe="1m", limit=14, retries=3):
    """
    Holt OHLCV-Daten für ein Handelspaar mit Fehlerbehandlung und Wiederholungen.
    """
    for attempt in range(retries):
        try:
            candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            return [c[4] for c in candles]  # Nur 'close'-Preise zurückgeben
        except Exception as e:
            logging.warning(f"Fehler beim Abrufen der Candle-Daten für {symbol}: {e}")
            if attempt < retries - 1:
                logging.info(f"Erneuter Versuch für {symbol} in 5 Sekunden...")
                time.sleep(5)
            else:
                logging.error(f"Maximale Versuche für {symbol} erreicht. Überspringe.")
                return None

def process_pairs():
    """
    Verarbeitet alle aktiven Handelspaare: Abrufen von Daten, RSI-Berechnung, Logging.
    """
    logging.info("Lade aktive Handelspaare...")
    pairs = load_active_pairs()  # Paare aus der Datenbank laden
    if not pairs:
        logging.warning("Keine aktiven Handelspaare gefunden.")
        return

    for symbol in pairs:
        try:
            logging.info(f"Verarbeite Handelspaar: {symbol}")

            # 1. Abrufen der Candle-Daten
            closes = fetch_candle_data(symbol)
            if closes is None or len(closes) < 14:
                logging.warning(f"Unzureichende Daten für {symbol}. Überspringe.")
                continue

            # 2. RSI-Berechnung
            rsi = calculate_rsi(closes)
            signal = "BUY" if rsi < 30 else "SELL" if rsi > 70 else "HOLD"
            action = "Trade ausgeführt" if signal in ["BUY", "SELL"] else "Kein Trade"

            # 3. Ergebnisse in die Datenbank loggen
            log_to_db(symbol, rsi, signal, action)
            logging.info(f"RSI: {rsi:.2f}, Signal: {signal}, Aktion: {action}")

        except Exception as e:
            logging.error(f"Fehler bei der Verarbeitung von {symbol}: {e}")

if __name__ == "__main__":
    try:
        while True:
            logging.info("Starte Verarbeitung aller Handelspaare...")
            process_pairs()  # Alle Paare verarbeiten
            logging.info("Verarbeitung abgeschlossen. Warte 10 Sekunden...")
            time.sleep(10)  # Pause zwischen Verarbeitungszyklen
    except KeyboardInterrupt:
        logging.info("Bot wurde gestoppt.")
    except Exception as e:
        logging.error(f"Unerwarteter Fehler: {e}")

