import sqlite3
import logging

DB_FILE = "trading_data.db"

def initialize_db():
    """
    Erstellt die notwendige Datenbankstruktur, falls diese noch nicht existiert.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Tabelle für Handelssignale
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pair TEXT,
            timestamp INTEGER,
            rsi REAL,
            signal TEXT,
            action TEXT,
            profit REAL DEFAULT 0
        )
        """)

        logging.info("Datenbank und Tabellen initialisiert.")
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Fehler beim Initialisieren der Datenbank: {e}")

def log_to_db(pair, rsi, signal, action, profit=0):
    """
    Speichert die Handelssignale und Aktionen in der Datenbank.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Daten einfügen
        cursor.execute("""
        INSERT INTO trades (pair, timestamp, rsi, signal, action, profit)
        VALUES (?, strftime('%s', 'now'), ?, ?, ?, ?)
        """, (pair, rsi, signal, action, profit))

        logging.info(f"Handelssignal für {pair} in die Datenbank geschrieben.")
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Fehler beim Speichern in die Datenbank: {e}")

def load_active_pairs():
    """
    Gibt eine Liste aktiver Handelspaare aus der Datenbank zurück.
    Fürs Testen können wir hier Dummy-Daten zurückgeben.
    """
    try:
        return ["BTC/USDT", "ETH/USDT", "LTC/USDT", "BNB/USDT"]  # Statische Testdaten
    except Exception as e:
        logging.error(f"Fehler beim Laden der aktiven Paare: {e}")
        return []
