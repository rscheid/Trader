import logging
from database import log_to_db, load_active_pairs
from trading_logic import setup_exchange, calculate_rsi
from dotenv import load_dotenv
import os
import time

# Logging konfigurieren
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

# Binance-Setup
load_dotenv()
API_KEY = os.getenv("TESTNET_API_KEY")
SECRET_KEY = os.getenv("TESTNET_SECRET")
exchange = setup_exchange(API_KEY, SECRET_KEY)

def process_pairs():
    pairs = load_active_pairs()
    logging.info(f"Geladene Paare: {len(pairs)} gefunden.")

    if not pairs:
        logging.warning("Keine aktiven Handelspaare gefunden.")
        return

    for symbol in pairs:
        try:
            logging.info(f"Verarbeite Paar: {symbol}")
            candles = exchange.fetch_ohlcv(symbol, timeframe="1m", limit=14)
            closes = [c[4] for c in candles]
            rsi = calculate_rsi(closes)
            signal = "BUY" if rsi < 30 else "SELL" if rsi > 70 else "HOLD"
            action = "Trade ausgeführt" if signal in ["BUY", "SELL"] else "Kein Trade"
            log_to_db(symbol, rsi, signal, action)
            logging.info(f"RSI: {rsi:.2f}, Signal: {signal}, Aktion: {action}")
        except Exception as e:
            logging.error(f"Fehler bei der Verarbeitung von {symbol}: {e}")

if __name__ == "__main__":
    try:
        while True:
            process_pairs()
            logging.info("Warte 10 Sekunden...")
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Bot wurde gestoppt.")

