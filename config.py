import os

# Binance API-Konfiguration aus Umgebungsvariablen
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")

# Binance Testnet aktivieren
TESTNET = True

# Pfade für Daten und Logs
DATA_PATH = "/root/home/trading-server-binance/data/"
LOG_PATH = "/root/home/trading-server-binance/logs/"

if __name__ == "__main__":
    if not API_KEY or not API_SECRET:
        print("FEHLER: API-Keys wurden nicht korrekt geladen.")
    else:
        print("API-Keys erfolgreich geladen!")
        print(f"API_KEY: {API_KEY}")
        print(f"API_SECRET: {API_SECRET}")
