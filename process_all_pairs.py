import logging
from database import log_to_db, load_active_pairs
from trading_logic import setup_exchange, calculate_rsi
from dotenv import load_dotenv
import os
import ccxt
import time

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Binance-Setup
load_dotenv()
API_KEY = os.getenv("TESTNET_API_KEY")
SECRET_KEY = os.getenv("TESTNET_SECRET")
exchange = setup_exchange(API_KEY, SECRET_KEY)

def process_pairs():
    """
    Verarbeitet alle aktiven Handelspaare und loggt RSI-Signale.
    """
    pairs = load_active_pairs()
    logging.info(f"{len(pairs)} aktive Paare geladen.")  # Debugging

    if not pairs:
        logging.warning("Keine aktiven Handelspaare gefunden.")
        return

    for idx, symbol in enumerate(pairs[:10], start=1):  # Begrenzung auf die ersten 10 Paare
        try:
            logging.info(f"({idx}/{len(pairs)}) Verarbeite Paar: {symbol}")

            # Abrufen von Candle-Daten
            candles = exchange.fetch_ohlcv(symbol, timeframe="1m", limit=14)
            if not candles:
                logging.warning(f"Keine Daten für {symbol} gefunden.")
                continue

            closes = [c[4] for c in candles]
            logging.info(f"Schlusskurse für {symbol}: {closes}")

            # RSI-Berechnung
            rsi = calculate_rsi(closes)
            signal = "BUY" if rsi < 30 else "SELL" if rsi > 70 else "HOLD"
            action = "Trade ausgeführt" if signal in ["BUY", "SELL"] else "Kein Trade"

            # In die Datenbank loggen
            log_to_db(symbol, rsi, signal, action)
            logging.info(f"RSI: {rsi:.2f}, Signal: {signal}, Aktion: {action}")

        except Exception as e:
            logging.error(f"Fehler bei der Verarbeitung von {symbol}: {e}")
            # Verarbeitung des nächsten Paares fortsetzen

if __name__ == "__main__":
    try:
        while True:
            logging.info("Starte Verarbeitung der Handelspaare...")
            process_pairs()
            logging.info("Verarbeitung abgeschlossen. Warte 10 Sekunden...")
            time.sleep(10)
    except KeyboardInterrupt:
        logging.info("Bot wurde gestoppt.")

