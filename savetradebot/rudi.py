import sqlite3
import logging
import time
import argparse
from trading_utility import fetch_candles, calculate_rsi, calculate_profit, update_ki_model

# Argumente parsen
parser = argparse.ArgumentParser()
parser.add_argument("--log-level", default="INFO", help="Setze das Log-Level (DEBUG, INFO, WARNING, ERROR)")
args = parser.parse_args()

# Logging konfigurieren
log_level = getattr(logging, args.log_level.upper(), logging.INFO)
logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

# Test-Log
logging.debug("Test-Log: Debugging ist aktiviert.")

# Datenbankverbindung herstellen
DB_FILE = 'trading_data.db'
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Datenbankstruktur sicherstellen
cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pair TEXT,
    timestamp INTEGER,
    rsi REAL,
    signal TEXT,
    action TEXT,
    value_usdt REAL,
    fees_usdt REAL,
    profit REAL
)
""")
logging.info("Datenbank und Tabelle 'trades' geprüft oder erstellt.")

# Handelslogik
PAIRS = ["BTC/USDT", "ETH/USDT", "LTC/USDT", "BNB/USDT"]
logging.debug(f"PAIRS: {PAIRS}")

def process_pair(pair):
    try:
        logging.debug(f"Starte Verarbeitung für: {pair}")

        # Historische Kerzen abrufen
        candles = fetch_candles(pair)
        close_prices = [float(c[4]) for c in candles]  # Sicherstellen, dass die Preise Floats sind
        logging.debug(f"{pair} - Erste 5 Close-Preise: {close_prices[:5]}")

        # RSI berechnen
        rsi = calculate_rsi(close_prices)
        logging.info(f"{pair} - RSI: {rsi:.2f}")

        # Signal bestimmen
        if rsi < 30:
            signal = "BUY"
        elif rsi > 70:
            signal = "SELL"
        else:
            signal = "HOLD"

        # Letzten Schlusskurs (last_price) aus den Candle-Daten extrahieren
        last_price = close_prices[-1]  # Aktueller Schlusskurs
        fee_percent = 0.001  # Beispiel-Gebührensatz (0.1%)

        # Profit berechnen
        profit = calculate_profit(last_price, fee_percent, signal)
        is_profitable = profit > 0
        logging.debug(f"{pair} - Profit: {profit}, Is Profitable: {is_profitable}, Signal: {signal}, RSI: {rsi}")

        action = signal if is_profitable else "NO_ACTION"

        # Gebührenberechnung
        value_usdt = last_price
        fees_usdt = last_price * fee_percent

        # Datenbankeintrag
        cursor.execute("""
        INSERT INTO trades (pair, timestamp, rsi, signal, action, value_usdt, fees_usdt, profit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (pair, int(time.time()), rsi, signal, action, value_usdt, fees_usdt, profit))
        conn.commit()
        logging.info(f"Daten gespeichert: {pair}, Aktion: {action}, Profit: {profit:.2f}")

        # KI-Modell aktualisieren
        update_ki_model(pair, rsi, signal, profit)

    except Exception as e:
        logging.error(f"Fehler beim Verarbeiten von {pair}: {e}", exc_info=True)

# Hauptlogik
try:
    logging.info("Starte Rudi-Bot auf Level 3...")
    for pair in PAIRS:
        process_pair(pair)
    logging.info("Rudi-Bot abgeschlossen.")
except Exception as e:
    logging.error(f"Kritischer Fehler im Hauptprozess: {e}", exc_info=True)
finally:
    conn.close()
