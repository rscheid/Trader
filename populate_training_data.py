import sqlite3

DB_PATH = "trading_data.db"

def populate_training_data():
    """
    Füllt die training_data-Tabelle mit Werten aus der trades-Tabelle.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Daten aus der trades-Tabelle kopieren
        cursor.execute("""
            INSERT INTO training_data (timestamp, pair, rsi, profit)
            SELECT timestamp, pair, rsi, profit
            FROM trades
            WHERE profit IS NOT NULL
        """)
        conn.commit()

        # Anzahl eingefügter Datensätze prüfen
        count = cursor.rowcount
        print(f"{count} Datensätze erfolgreich in training_data eingefügt.")

    except Exception as e:
        print(f"Fehler beim Einfügen von Daten: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    try:
        populate_training_data()
    except KeyboardInterrupt:
        print("Skript wurde manuell unterbrochen.")
