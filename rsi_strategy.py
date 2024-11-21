import logging
import time
import os
from dotenv import load_dotenv
from database import initialize_database, log_to_db
from trading_logic import setup_exchange, calculate_rsi

# .env laden
load_dotenv()

API_KEY = os.getenv("TESTNET_API_KEY")
SECRET_KEY = os.getenv("TESTNET_SECRET")

if not API_KEY or not SECRET_KEY:
    raise ValueError("API_KEY und SECRET_KEY müssen in der .env-Datei definiert sein!")

# Logging-Verzeichnis und Datei konfigurieren
LOG_DIRECTORY = "/app/logs"
LOG_FILE = os.path.join(LOG_DIRECTORY, "trading_bot.log")
os.makedirs(LOG_DIRECTORY, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(LOG_FILE, mode="a")
    ]
)

# Binance konfigurieren
exchange = setup_exchange(API_KEY, SECRET_KEY)

# Datenbank initialisieren
initialize_database()

# Hauptlogik
def main():
    logging.info("RSI-Bot gestartet.")
    symbol = "BTC/USDT"
    timeframe = "1m"
    try:
        candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=14)
        closes = [c[4] for c in candles]
        rsi = calculate_rsi(closes)
        signal = "BUY" if rsi < 30 else "SELL" if rsi > 70 else "HOLD"
        action = "Trade ausgeführt" if signal in ["BUY", "SELL"] else "Kein Trade"
        log_to_db(symbol, rsi, signal, action)
        logging.info(f"RSI: {rsi:.2f}, Signal: {signal}, Aktion: {action}")
    except Exception as e:
        logging.error(f"Fehler im Hauptprozess: {e}")

if __name__ == "__main__":
    while True:
        main()
        time.sleep(10)

