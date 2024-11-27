import sqlite3
import logging

def load_active_pairs():
    """
    Lädt alle aktiven Handelspaare aus der Tabelle active_pairs.
    """
    try:
        conn = sqlite3.connect("trading_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT symbol FROM active_pairs")
        pairs = [row[0] for row in cursor.fetchall()]
        conn.close()
        return pairs
    except Exception as e:
        logging.error(f"Fehler beim Laden der aktiven Paare: {e}")
        return []

if __name__ == "__main__":
    pairs = load_active_pairs()
    print(f"Geladene Paare: {pairs}")
