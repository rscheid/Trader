import ccxt
import logging
from dotenv import load_dotenv
import os
import sqlite3
import time
import csv

# .env-Datei laden
load_dotenv()

# Binance Testnet-API-Schlüssel aus Umgebungsvariablen lesen
API_KEY = os.getenv("TESTNET_API_KEY")
SECRET_KEY = os.getenv("TESTNET_SECRET")

# Verbindung zur Binance Testnet API herstellen
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
    'enableRateLimit': True,
})

# Testnet aktivieren
exchange.set_sandbox_mode(True)

# Verbindung zur SQLite-Datenbank
db_path = "trading_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tabelle erstellen, falls sie nicht existiert
cursor.execute("""
CREATE TABLE IF NOT EXISTS trading_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    symbol TEXT,
    rsi REAL,
    signal TEXT,
    action TEXT
)
""")
conn.commit()

# Logger konfigurieren
log_directory = '/app'
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, 'trading_bot.log')

try:
    file_handler = logging.FileHandler(log_file, mode='a')  # Append-Modus
    handlers = [logging.StreamHandler(), file_handler]
except Exception as e:
    print(f"Fehler beim Erstellen des FileHandlers: {e}")
    handlers = [logging.StreamHandler()]

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=handlers
)

logging.info("Logging initialisiert. Dies ist ein Testeintrag.")

# Beispiel: Alle Paare aus der CSV-Datei laden
pairs = []
with open("pair_rankings.csv", "r") as file:
    reader = csv.DictReader(file)
    pairs = [row["pair"] for row in reader]

# RSI-Berechnung
def calculate_rsi(closes, period=14):
    delta = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [d for d in delta if d > 0]
    losses = [-d for d in delta if d < 0]

    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 1  # Kein Verlust = künstlich 1

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Signal-Berechnung
def get_rsi_signal(symbol="BTC/USDT", timeframe="1m", limit=14):
    try:
        candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        closes = [c[4] for c in candles]
        rsi = calculate_rsi(closes)

        logging.info(f"RSI berechnet: {rsi:.2f} für {symbol}")

        if rsi < 30:
            logging.info("Signal: BUY")
            return "BUY", rsi
        elif rsi > 50:
            logging.info("Signal: SELL")
            return "SELL", rsi
        else:
            logging.info("Signal: HOLD")
            return "HOLD", rsi
    except Exception as e:
        logging.error(f"Fehler in get_rsi_signal: {e}")
        return "ERROR", None

# Logging in die Datenbank
def log_to_db(symbol, rsi, signal, action):
    try:
        cursor.execute("""
        INSERT INTO trading_data (symbol, rsi, signal, action)
        VALUES (?, ?, ?, ?)
        """, (symbol, rsi, signal, action))
        conn.commit()
        logging.info(f"Eintrag in die Datenbank: Symbol={symbol}, RSI={rsi}, Signal={signal}, Action={action}")
    except Exception as e:
        logging.error(f"Fehler beim Schreiben in die Datenbank: {e}")

# Handelsstrategie anwenden
def execute_trade(signal, symbol="BTC/USDT", amount=0.001):
    try:
        action = "Trade ausgeführt" if signal in ["BUY", "SELL"] else "Kein Trade"
        log_to_db(symbol, rsi, signal, action)

        if signal == "BUY":
            order = exchange.create_market_buy_order(symbol, amount)
            logging.info(f"BUY-Order erfolgreich: {order}")
            return f"BUY-Order erfolgreich: {order}"

        elif signal == "SELL":
            order = exchange.create_market_sell_order(symbol, amount)
            logging.info(f"SELL-Order erfolgreich: {order}")
            return f"SELL-Order erfolgreich: {order}"

        else:
            logging.info("Signal: HOLD - Kein Trade ausgeführt.")
            return "HOLD - Kein Trade ausgeführt."
    except Exception as e:
        logging.error(f"Fehler bei {signal}-Order: {e}")
        return f"Fehler bei {signal}-Order: {e}"

# Hauptausführung
if __name__ == "__main__":
    amount = 0.001

    for pair in pairs:
        signal, rsi = get_rsi_signal(pair)
        if signal != "ERROR":
            action = "Trade ausgeführt" if signal in ["BUY", "SELL"] else "Kein Trade"
            log_to_db(pair, rsi, signal, action)

            if signal == "BUY":
                logging.info(f"Starte BUY-Order: {pair}, Menge={amount}")
            elif signal == "SELL":
                logging.info(f"Starte SELL-Order: {pair}, Menge={amount}")
        else:
            logging.error("Fehler bei der Berechnung des RSI")

        # 60 Sekunden warten vor der nächsten Berechnung
        time.sleep(60)
