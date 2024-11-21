import sqlite3
import logging

DB_PATH = "trading_data.db"

def connect_db():
    try:
        return sqlite3.connect(DB_PATH)
    except sqlite3.Error as e:
        logging.error(f"Fehler beim Herstellen der DB-Verbindung: {e}")
        raise

def initialize_database():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS trading_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            symbol TEXT,
            rsi REAL,
            signal TEXT,
            action TEXT
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS active_pairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE NOT NULL
        )
        """)
        conn.commit()
        logging.info("Datenbank erfolgreich initialisiert.")
    except sqlite3.Error as e:
        logging.error(f"Fehler bei der Initialisierung der Datenbank: {e}")
        raise
    finally:
        conn.close()

def log_to_db(symbol, rsi, signal, action):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO trading_data (symbol, rsi, signal, action)
        VALUES (?, ?, ?, ?)
        """, (symbol, rsi, signal, action))
        conn.commit()
        logging.info(f"Daten in DB gespeichert: {symbol}, RSI={rsi}, Signal={signal}, Aktion={action}")
    except sqlite3.Error as e:
        logging.error(f"Fehler beim Schreiben in die Datenbank: {e}")
        raise
    finally:
        conn.close()

def save_symbols_to_db(symbols):
    try:
        conn = connect_db()
        cursor = conn.cursor()
        for symbol in symbols:
            cursor.execute("""
            INSERT OR IGNORE INTO active_pairs (symbol)
            VALUES (?)
            """, (symbol,))
        conn.commit()
        logging.info(f"{len(symbols)} Handelspaare in die Datenbank eingefügt.")
    except sqlite3.Error as e:
        logging.error(f"Fehler beim Speichern der Handelspaare: {e}")
        raise
    finally:
        conn.close()

def load_active_pairs():
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT symbol FROM active_pairs")
        pairs = [row[0] for row in cursor.fetchall()]
        logging.info(f"{len(pairs)} aktive Handelspaare aus der Datenbank geladen.")
        return pairs
    except sqlite3.Error as e:
        logging.error(f"Fehler beim Laden der aktiven Handelspaare: {e}")
        raise
    finally:
        conn.close()

