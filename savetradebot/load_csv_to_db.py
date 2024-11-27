import sqlite3
import pandas as pd

def load_csv_to_db(csv_file, db_file):
    """Lädt Daten aus einer CSV-Datei in eine SQLite-Datenbank."""
    try:
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # CSV-Datei in ein DataFrame laden
        df = pd.read_csv(csv_file)

        # Durch die DataFrame-Zeilen iterieren und in die Datenbank einfügen
        for index, row in df.iterrows():
            pair = row['pair']
            avg_volume = row['avg_volume']
            price_stability = row['price_stability']

            # SQL-Abfrage zum Einfügen der Daten
            cursor.execute('''
                INSERT INTO active_pairs (pair, avg_volume, price_stability)
                VALUES (?, ?, ?)
            ''', (pair, avg_volume, price_stability))

        # Änderungen speichern und Verbindung schließen
        conn.commit()
        print(f"Erfolgreich {len(df)} Datensätze aus {csv_file} in die Datenbank geladen.")
    except Exception as e:
        print(f"Fehler beim Laden der CSV-Datei in die Datenbank: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Pfade zu den Dateien
    csv_file = 'pair_rankings.csv'
    db_file = 'trading_data.db'

    # Funktion zum Laden der CSV-Daten in die Datenbank aufrufen
    load_csv_to_db(csv_file, db_file)
