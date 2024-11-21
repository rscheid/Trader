import logging
import time
from binance_api import setup_exchange, fetch_candles
from trading_logic import calculate_rsi
from database import initialize_db, log_to_db
from dotenv import load_dotenv
import os

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Binance-Setup
load_dotenv()
API_KEY = os.getenv("TESTNET_API_KEY")
SECRET_KEY = os.getenv("TESTNET_SECRET")
exchange = setup_exchange(API_KEY, SECRET_KEY, testnet=True)

# Datenbank initialisieren
initialize_db()

def process_pairs(pairs):
    """
    Verarbeitet alle aktiven Handelspaare und loggt RSI-Signale.
    """
    logging.info(f"{len(pairs)} aktive Paare geladen.")

    for idx, pair in enumerate(pairs, start=1):
        try:
            logging.info(f"({idx}/{len(pairs)}) Verarbeite Paar: {pair}")

            # Candle-Daten abrufen
            candles = fetch_candles(exchange, pair, timeframe="1m", limit=14)
            if not candles:
                logging.warning(f"Keine Daten für {pair} gefunden. Überspringe.")
                continue

            # Schlusskurse extrahieren
            closes = [c[4] for c in candles]
            if len(closes) < 14:
                logging.warning(f"Nicht genügend Schlusskurse für {pair}. Überspringe.")
                continue

            # RSI berechnen
            rsi = calculate_rsi(closes)
            if rsi is None:
                logging.warning(f"RSI konnte nicht berechnet werden für {pair}.")
                continue

            # Signal generieren
            signal = "BUY" if rsi < 30 else "SELL" if rsi > 70 else "HOLD"
            action = "Trade ausgeführt" if signal in ["BUY", "SELL"] else "Kein Trade"

            # Ergebnisse loggen und in die DB schreiben
            logging.info(f"{pair} - RSI: {rsi:.2f}, Signal: {signal}, Aktion: {action}")
            log_to_db(pair, rsi, signal, action, 0)  # Profit auf 0, da hier nur Signale berechnet werden

            # Warten, um API-Limits einzuhalten
            time.sleep(1)

        except Exception as e:
            logging.error(f"Unerwarteter Fehler bei {pair}: {e}. Überspringe.")
            continue

if __name__ == "__main__":
    try:
        # Liste der Handelspaare definieren
        pairs = ["BTC/USDT", "ETH/USDT", "LTC/USDT", "BNB/USDT"]  # Beispielpaare
        while True:
            logging.info("Starte Verarbeitung der Handelspaare...")
            process_pairs(pairs)
            logging.info("Verarbeitung abgeschlossen. Warte 60 Sekunden...")
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("Bot wurde gestoppt.")
