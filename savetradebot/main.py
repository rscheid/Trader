import logging
import time
from fetch_symbols import fetch_binance_symbols
from database import save_symbols_to_db, initialize_database
from process_all_pairs import process_pairs

# Logging konfigurieren
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    logging.info("Trading-Bot gestartet.")

    # Datenbank initialisieren
    initialize_database()

    # Aktuelle Handelspaare abrufen und speichern
    logging.info("Handelspaare abrufen...")
    symbols = fetch_binance_symbols()
    save_symbols_to_db(symbols)
    logging.info(f"{len(symbols)} Handelspaare erfolgreich gespeichert.")

    # Multi-Pair-Verarbeitung
    while True:
        logging.info("Beginne Verarbeitung aller Handelspaare.")
        process_pairs()
        logging.info("Verarbeitung abgeschlossen. Warte 10 Sekunden.")
        time.sleep(10)

if __name__ == "__main__":
    main()






#from fetch_historical import fetch_data
#from calculate_indicators import calculate_and_store_indicators

#def main():
#    fetch_data()
#    calculate_and_store_indicators()

#if __name__ == "__main__":
#    main()
