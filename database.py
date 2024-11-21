import sqlite3
import logging

DB_PATH = "trading_data.db"

def connect_db():
    return sqlite3.connect(DB_PATH)

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
        logging.info("Datenbank initialisiert.")
    except Exception as e:
        logging.error(f"Fehler bei der Initialisierung der Datenbank: {e}")
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
    except Exception as e:
        logging.error(f"Fehler beim Schreiben in die Datenbank: {e}")
    finally:
        conn.close()
