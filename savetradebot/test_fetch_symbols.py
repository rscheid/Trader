import logging
from binance_api import setup_exchange
from trading_logic import fetch_binance_symbols
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

# Test: Abruf der Handelspaare
try:
    logging.info("Starte Test für `fetch_binance_symbols()`...")
    pairs = fetch_binance_symbols(exchange)
    if pairs:
        logging.info(f"Erfolgreich {len(pairs)} Handelspaare abgerufen.")
        logging.info(f"Erste 5 Handelspaare: {pairs[:5]}")
    else:
        logging.warning("Keine Handelspaare abgerufen.")
except Exception as e:
    logging.error(f"Fehler beim Abrufen der Handelspaare: {e}", exc_info=True)
