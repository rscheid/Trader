import sqlite3
import logging

# Konfiguration des Logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Datenbankpfad
DB_PATH = "trading_data.db"

def check_table_schema():
    """
    Prüft das Schema der Tabelle `training_data`.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Abfrage des Schemas der Tabelle
        cursor.execute("PRAGMA table_info(training_data);")
        schema = cursor.fetchall()

        logging.info("Schema der Tabelle `training_data`:")
        for col in schema:
            logging.info(f"Spalte: {col[1]}, Typ: {col[2]}")

        conn.close()
    except Exception as e:
        logging.error(f"Fehler beim Abrufen des Tabellenschemas: {e}")

def check_data_counts():
    """
    Prüft die Anzahl der Einträge in der Tabelle `training_data`.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Gesamtanzahl der Einträge
        cursor.execute("SELECT COUNT(*) FROM training_data;")
        count = cursor.fetchone()[0]
        logging.info(f"Gesamtanzahl der Einträge in `training_data`: {count}")

        conn.close()
    except Exception as e:
        logging.error(f"Fehler beim Abrufen der Anzahl der Einträge: {e}")

def check_missing_values():
    """
    Prüft auf fehlende Werte in wichtigen Spalten.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Fehlende RSI-Werte prüfen
        cursor.execute("SELECT COUNT(*) FROM training_data WHERE rsi IS NULL;")
        missing_rsi = cursor.fetchone()[0]
        logging.info(f"Einträge ohne RSI-Wert: {missing_rsi}")

        # Fehlende Signale prüfen
        cursor.execute("SELECT COUNT(*) FROM training_data WHERE signal IS NULL;")
        missing_signals = cursor.fetchone()[0]
        logging.info(f"Einträge ohne Signal: {missing_signals}")

        conn.close()
    except Exception as e:
        logging.error(f"Fehler beim Prüfen fehlender Werte: {e}")

def show_sample_data(limit=10):
    """
    Zeigt eine Vorschau der ersten `limit` Einträge in der Tabelle.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Vorschau der Daten
        cursor.execute(f"SELECT * FROM training_data LIMIT {limit};")
        rows = cursor.fetchall()
        logging.info(f"Erste {limit} Einträge der Tabelle `training_data`:")
        for row in rows:
            logging.info(row)

        conn.close()
    except Exception as e:
        logging.error(f"Fehler beim Abrufen der Datenvorschau: {e}")

if __name__ == "__main__":
    logging.info("Starte Validierung der Tabelle `training_data`...")
    check_table_schema()      # Schema prüfen
    check_data_counts()       # Anzahl der Einträge prüfen
    check_missing_values()    # Fehlende Werte prüfen
    show_sample_data()        # Vorschau der Daten anzeigen
