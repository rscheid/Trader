import time
import logging
from market_sync_and_fetch import sync_and_fetch  # Synchronisierung
# Füge weitere Module hinzu, wenn nötig

# Logging einrichten
logging.basicConfig(
    filename="trading_bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    while True:
        try:
            logging.info("Starte Synchronisierung der Märkte...")
            sync_and_fetch()
            logging.info("Synchronisierung abgeschlossen. Warte 5 Minuten.")
            time.sleep(300)  # 5 Minuten Pause
        except Exception as e:
            logging.error(f"Fehler in der Hauptschleife: {e}")
            logging.info("Versuche Neustart in 1 Minute...")
            time.sleep(60)  # Nach einem Fehler 1 Minute warten und dann Neustart

if __name__ == "__main__":
    main()
