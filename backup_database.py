import sqlite3
import os
from datetime import datetime

def backup_database(db_path='trading_data.db', backup_dir='backups'):
    """
    Erstellt ein Backup der SQLite-Datenbank.
    
    :param db_path: Pfad zur SQLite-Datenbank.
    :param backup_dir: Verzeichnis, in dem das Backup gespeichert wird.
    """
    try:
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)

        # Backup-Dateiname mit Zeitstempel
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(backup_dir, f"trading_data_backup_{timestamp}.db")

        # Backup durchführen
        conn = sqlite3.connect(db_path)
        with sqlite3.connect(backup_file) as backup_conn:
            conn.backup(backup_conn)
        
        print(f"Backup erfolgreich: {backup_file}")
    except Exception as e:
        print(f"Fehler beim Erstellen des Backups: {str(e)}")
    finally:
        conn.close()

if __name__ == "__main__":
    # Backup der Datenbank erstellen
    backup_database()
