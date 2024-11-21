import ccxt
from dotenv import load_dotenv
import os

# API-Schlüssel laden
load_dotenv()
API_KEY = os.getenv("TESTNET_API_KEY")
SECRET_KEY = os.getenv("TESTNET_SECRET")

# Binance Testnet-Setup
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
    'enableRateLimit': True,
})

exchange.set_sandbox_mode(True)  # Testnet aktivieren

def check_balance():
    """
    Überprüft das verfügbare Guthaben im Testnet.
    """
    try:
        balance = exchange.fetch_balance()
        print("Verfügbare Guthaben im Testnet:")
        for asset, details in balance['total'].items():
            if details > 0:
                print(f"{asset}: {details}")
    except Exception as e:
        print(f"Fehler beim Abrufen des Guthabens: {e}")

if __name__ == "__main__":
    check_balance()
