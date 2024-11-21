import sqlite3
import logging

# Konfiguration
DB_PATH = "trading_data.db"

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def connect_db():
    """
    Stellt eine Verbindung zur SQLite-Datenbank her.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        logging.debug(f"Verbindung zur Datenbank {DB_PATH} erfolgreich hergestellt.")
        return conn
    except sqlite3.Error as e:
        logging.error(f"Fehler beim Herstellen der DB-Verbindung: {e}")
        raise

def initialize_database():
    """
    Initialisiert die notwendigen Tabellen in der Datenbank.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()

        # Tabellen erstellen
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
    """
    Fügt Handelsdaten in die Tabelle 'trading_data' ein.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO trading_data (symbol, rsi, signal, action)
        VALUES (?, ?, ?, ?)
        """, (symbol, rsi, signal, action))
        conn.commit()
        logging.info(f"Daten in DB gespeichert: {symbol}, RSI={rsi}, Signal={signal}, Aktion={action}")
        return True
    except sqlite3.Error as e:
        logging.error(f"Fehler beim Schreiben in die Datenbank: {e}")
        return False
    finally:
        conn.close()

def save_symbols_to_db(symbols):
    """
    Speichert Handelspaare in der Tabelle 'active_pairs'.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        for symbol in symbols:
            cursor.execute("""
            INSERT OR IGNORE INTO active_pairs (symbol)
            VALUES (?)
            """, (symbol,))
        conn.commit()
        if symbols:
            logging.info(f"{len(symbols)} Handelspaare in die Datenbank eingefügt.")
        else:
            logging.info("Keine neuen Handelspaare zum Einfügen.")
        return True
    except sqlite3.Error as e:
        logging.error(f"Fehler beim Speichern der Handelspaare: {e}")
        return False
    finally:
        conn.close()

def load_active_pairs():
    """
    Lädt alle aktiven Handelspaare aus der Tabelle 'active_pairs'.
    """
    try:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT symbol FROM active_pairs")
        pairs = [row[0] for row in cursor.fetchall()]
        if not pairs:
            logging.warning("Keine aktiven Handelspaare gefunden.")
        else:
            logging.info(f"{len(pairs)} aktive Handelspaare aus der Datenbank geladen.")
        return pairs
    except sqlite3.Error as e:
        logging.error(f"Fehler beim Laden der aktiven Handelspaare: {e}")
        return []
    finally:
        conn.close()
