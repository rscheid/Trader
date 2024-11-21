import logging
import time
from database import log_to_db, load_active_pairs
from trading_logic import setup_exchange, fetch_binance_symbols, calculate_rsi
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
exchange = setup_exchange(API_KEY, SECRET_KEY)
symbols = fetch_binance_symbols(exchange)
print(f"Gefundene Symbole: {symbols}")

def process_pairs():
    """
    Verarbeitet alle aktiven Handelspaare und loggt RSI-Signale.
    """
    pairs = load_active_pairs()  # Paare aus der Datenbank laden
    logging.info(f"{len(pairs)} aktive Paare geladen.")

    if not pairs:
        logging.warning("Keine aktiven Handelspaare gefunden.")
        return

    for idx, pair in enumerate(pairs, start=1):
        try:
            logging.info(f"({idx}/{len(pairs)}) Verarbeite Paar: {pair}")

            # Candle-Daten abrufen
            candles = exchange.fetch_ohlcv(pair, timeframe="1m", limit=14)
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
            log_to_db(pair, rsi, signal, action)

            # Dummy-Trade-Logik
            if signal == "BUY":
                logging.info(f"Kaufe {pair}. (Simulation)")
            elif signal == "SELL":
                logging.info(f"Verkaufe {pair}. (Simulation)")
            else:
                logging.info(f"Keine Aktion für {pair}. (HOLD)")

            # Warten, um API-Limits einzuhalten
            time.sleep(1)

        except ccxt.NetworkError as e:
            logging.error(f"Netzwerkfehler bei {pair}: {e}. Überspringe.")
            continue
        except ccxt.BaseError as e:
            logging.error(f"API-Fehler bei {pair}: {e}. Überspringe.")
            continue
        except Exception as e:
            logging.error(f"Unerwarteter Fehler bei {pair}: {e}. Überspringe.")
            continue

def fetch_binance_symbols(exchange):
    """
    Ruft alle Handelspaare von Binance ab.
    """
    try:
        markets = exchange.load_markets()
        symbols = list(markets.keys())
        return symbols
    except Exception as e:
        print(f"Fehler beim Abrufen der Handelspaare: {e}")
        return []


if __name__ == "__main__":
    try:
        while True:
            logging.info("Starte Verarbeitung der Handelspaare...")
            process_pairs()
            logging.info("Verarbeitung abgeschlossen. Warte 60 Sekunden...")
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("Bot wurde gestoppt.")
