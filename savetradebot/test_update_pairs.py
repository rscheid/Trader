import logging
from dotenv import load_dotenv
from database import initialize_pairs_table
from trading_logic import fetch_binance_symbols
from binance_api import setup_exchange
import sqlite3
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

# Test: Datenbank-Update
try:
    logging.info("Starte Test für Datenbank-Update...")
    initialize_pairs_table(exchange)
    pairs = fetch_binance_symbols(exchange)

    if pairs:
        conn = sqlite3.connect("trading_data.db")
        cursor = conn.cursor()

        # Alle Paare inaktiv setzen
        cursor.execute("UPDATE pairs SET active = 0")
        conn.commit()
        logging.info("Alle Handelspaare vorübergehend inaktiv gesetzt.")

        # Neue Paare hinzufügen
        for pair in pairs:
            cursor.execute("INSERT OR IGNORE INTO pairs (pair, active) VALUES (?, 1)", (pair,))
            cursor.execute("UPDATE pairs SET active = 1 WHERE pair = ?", (pair,))

        conn.commit()
        logging.info(f"{len(pairs)} Handelspaare in die Datenbank eingefügt oder aktualisiert.")
        conn.close()
    else:
        logging.warning("Keine Handelspaare zum Einfügen vorhanden.")
except Exception as e:
    logging.error(f"Fehler beim Datenbank-Update: {e}", exc_info=True)
