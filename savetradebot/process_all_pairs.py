import logging
import os
import time
from dotenv import load_dotenv
from database import log_to_db, load_active_pairs, initialize_pairs_table
from trading_logic import calculate_rsi, fetch_binance_symbols
from binance_api import setup_exchange, fetch_candles
from train_lstm import train_model
import sqlite3

# Logging konfigurieren
logging.basicConfig(
    level=logging.DEBUG,  # Debug-Level für detaillierte Logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Binance-Setup
load_dotenv()
API_KEY = os.getenv("TESTNET_API_KEY")
SECRET_KEY = os.getenv("TESTNET_SECRET")
exchange = setup_exchange(API_KEY, SECRET_KEY, testnet=True)

BATCH_SIZE = 300  # Anzahl der Paare, die pro Zyklus verarbeitet werden

def update_pairs():
    """
    Aktualisiert die Liste der Handelspaare in der Datenbank.
    """
    try:
        logging.info("Starte Aktualisierung der Handelspaare von der Binance-API...")
        initialize_pairs_table(exchange)

        # Abruf der aktuellen Handelspaare von Binance
        current_pairs = fetch_binance_symbols(exchange)
        logging.debug(f"Aktuelle Paare abgerufen: {len(current_pairs)}")
        logging.debug(f"Erste 5 Paare: {current_pairs[:5]}")

        conn = sqlite3.connect("trading_data.db")
        cursor = conn.cursor()

        # Alle Paare inaktiv setzen
        cursor.execute("UPDATE pairs SET active = 0")
        conn.commit()
        logging.info("Alle Handelspaare vorübergehend inaktiv gesetzt.")

        # Neue Paare hinzufügen oder aktivieren
        for pair in current_pairs:
            cursor.execute("INSERT OR IGNORE INTO pairs (pair, active) VALUES (?, 1)", (pair,))
            cursor.execute("UPDATE pairs SET active = 1 WHERE pair = ?", (pair,))

        conn.commit()
        conn.close()
        logging.info(f"{len(current_pairs)} Handelspaare aktualisiert und synchronisiert.")

    except Exception as e:
        logging.error(f"Fehler bei der Aktualisierung der Handelspaare: {e}", exc_info=True)

def process_pairs(batch_start=0):
    """
    Verarbeitet eine Teilmenge der aktiven Handelspaare.
    """
    pairs = load_active_pairs()  # Paare aus der Datenbank laden
    if not pairs:
        logging.warning("Keine aktiven Handelspaare gefunden.")
        return batch_start  # Keine neuen Paare, starte beim aktuellen Index

    logging.info(f"{len(pairs)} aktive Paare geladen.")
    batch_end = batch_start + BATCH_SIZE
    current_batch = pairs[batch_start:batch_end]

    logging.info(f"Verarbeite Paare {batch_start} bis {batch_end}...")

    for idx, pair in enumerate(current_batch, start=batch_start + 1):
        try:
            logging.info(f"({idx}/{len(pairs)}) Verarbeite Paar: {pair}")

            # Kerzendaten abrufen
            candles = fetch_candles(exchange, pair, "1m", limit=14)
            if not candles or len(candles) < 14:
                logging.warning(f"Unzureichende Kerzendaten für {pair}: {candles}")
                continue

            # Schlusskurse extrahieren
            closes = [c[4] for c in candles if c[4] is not None]
            if len(closes) < 14:
                logging.warning(f"Ungültige Schlusskurse für {pair}: {closes}")
                continue

            # RSI berechnen
            rsi = calculate_rsi(closes)
            if rsi is None:
                logging.warning(f"RSI konnte nicht berechnet werden für {pair}.")
                continue

            # Zusätzliche Berechnungen
            last_price = closes[-1] if closes else 0.0
            price_change = closes[-1] - closes[0] if len(closes) > 1 else 0.0
            volume = sum(c[5] for c in candles if c[5] is not None)
            trade_fee = last_price * 0.001  # 0.1% Gebühren
            profit = price_change - trade_fee if rsi < 30 or rsi > 70 else 0.0

            # Signal generieren
            signal = "BUY" if rsi < 30 else "SELL" if rsi > 70 else "HOLD"
            action = "Trade ausgeführt" if signal in ["BUY", "SELL"] else "Kein Trade"

            # Simuliertes Trading
            if signal == "BUY":
                logging.info(f"Simulierter Kauf: {pair} - Preis: {last_price}")
            elif signal == "SELL":
                logging.info(f"Simulierter Verkauf: {pair} - Preis: {last_price}")
            else:
                logging.info(f"Keine Aktion für {pair} (HOLD).")

            # Ergebnisse loggen und in die DB schreiben
            log_to_db(
                pair=pair,
                rsi=rsi,
                signal=signal,
                action=action,
                last_price=last_price,
                trade_fee=trade_fee,
                price_change=price_change,
                volume=volume,
                timestamp=int(time.time()),
                profit=profit
            )

        except Exception as e:
            logging.error(f"Fehler bei der Verarbeitung von {pair}: {e}", exc_info=True)

    return batch_end if batch_end < len(pairs) else 0  # Zurücksetzen, wenn alle Paare verarbeitet wurden

if __name__ == "__main__":
    try:
        batch_start = 0
        while True:
            # Zielzeit für den nächsten Zyklus
            next_cycle_start = time.time() + 60

            logging.info(f"Neuer Zyklus gestartet um {time.strftime('%Y-%m-%d %H:%M:%S')}.")

            # Aktualisiere Handelspaare
            update_pairs()

            # Verarbeite eine Teilmenge der Handelspaare
            batch_start = process_pairs(batch_start)

            # Wartezeit berechnen
            current_time = time.time()
            sleep_time = max(next_cycle_start - current_time, 0)
            logging.info(f"Zyklus abgeschlossen. Warte {sleep_time:.2f} Sekunden bis zum nächsten Zyklus...")
            time.sleep(sleep_time)

    except KeyboardInterrupt:
        logging.info("Bot wurde gestoppt.")
    except Exception as e:
        logging.critical(f"Unbehandelter Fehler im Hauptprozess: {e}", exc_info=True)
