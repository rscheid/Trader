import logging
import os
import time
from dotenv import load_dotenv  # Lädt Umgebungsvariablen
from database import log_to_db, load_active_pairs, initialize_pairs_table  # Funktionen für die Datenbank
from binance_api import setup_exchange, fetch_candles  # Binance-spezifische Logik
from rsi_calculation import calculate_rsi  # RSI-Berechnung
from populate_training_data import populate_training_data  # Trainingsdaten aktualisieren

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

# Handelspaare in die Datenbank einfügen
initialize_pairs_table(exchange)


def process_pairs():
    """
    Verarbeitet alle aktiven Handelspaare und loggt RSI-Signale.
    """
    pairs = load_active_pairs()  # Paare aus der Datenbank laden
    if not pairs:
        logging.warning("Keine aktiven Handelspaare gefunden.")
        return

    logging.info(f"{len(pairs)} aktive Paare geladen.")

    for idx, pair in enumerate(pairs, start=1):
        try:
            logging.info(f"({idx}/{len(pairs)}) Verarbeite Paar: {pair}")

# Kerzendaten abrufen
candles = fetch_candles(exchange, pair, "1m", limit=14)
if not candles:
    logging.warning(f"Keine Kerzendaten für {pair}. Überspringe.")
    continue
if len(candles) < 14:
    logging.warning(f"Nicht genügend Schlusskurse für {pair} (nur {len(candles)} erhalten). Überspringe.")
    continue

# Schlusskurse und Volumen extrahieren
closes = [c[4] for c in candles]  # Index 4 für 'close' Preis
volumes = [c[5] for c in candles]  # Index 5 für 'volume'

# Berechnung absichern
try:
    rsi = calculate_rsi(closes)
    if rsi is None:
        logging.warning(f"RSI konnte für {pair} nicht berechnet werden. Überspringe.")
        continue
except Exception as e:
    logging.error(f"Fehler bei der RSI-Berechnung für {pair}: {e}")
    continue



            # Signal generieren
            signal = "BUY" if rsi < 30 else "SELL" if rsi > 70 else "HOLD"
            action = "Trade ausgeführt" if signal in ["BUY", "SELL"] else "Kein Trade"

            # Zusätzliche Berechnungen
            volumes = [c[5] for c in candles]  # Volumen aus den Kerzendaten
            last_close = closes[-1]  # Letzter Schlusskurs
            first_close = closes[0]  # Erster Schlusskurs in der Periode
            price_change = ((last_close - first_close) / first_close) * 100  # Prozentuale Preisänderung
            volume = sum(volumes)  # Gesamtvolumen in der Periode
            trade_fee = last_close * 0.001  # Beispiel: 0.1% Gebühr
            profit = price_change - (trade_fee if signal in ["BUY", "SELL"] else 0)  # Profit mit Abzug der Gebühr

            logging.debug(f"Berechnung: last_close={last_close}, first_close={first_close}, "
                          f"price_change={price_change}, volume={volume}, trade_fee={trade_fee}, profit={profit}")

            # Ergebnisse loggen und in die DB schreiben
            logging.info(f"{pair} - RSI: {rsi:.2f}, Signal: {signal}, Aktion: {action}")
            log_to_db(
                pair=pair,
                rsi=rsi,
                signal=signal,
                action=action,
                last_price=last_close,
                trade_fee=trade_fee,
                timestamp=int(time.time()),
                profit=profit,
                price_change=price_change,
                volume=volume
            )

            # Simulierte Aktion basierend auf dem Signal
            if signal == "BUY":
                logging.info(f"Kaufe {pair}. (Simulation)")
            elif signal == "SELL":
                logging.info(f"Verkaufe {pair}. (Simulation)")
            else:
                logging.info(f"Keine Aktion für {pair}. (HOLD)")

            # API-Limit einhalten
            time.sleep(1)

        except Exception as e:
            logging.error(f"Fehler bei der Verarbeitung von {pair}: {e}. Überspringe.")
            continue

    # Trainingsdaten aktualisieren
    populate_training_data()
    logging.info("Trainingsdaten wurden aktualisiert.")


if __name__ == "__main__":
    try:
        while True:
            logging.info("Starte Verarbeitung der Handelspaare...")
            process_pairs()
            logging.info("Verarbeitung abgeschlossen. Warte 60 Sekunden...")
            time.sleep(60)
    except KeyboardInterrupt:
        logging.info("Bot wurde gestoppt.")
