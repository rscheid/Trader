import sqlite3
import logging

DB_PATH = "trading_data.db"

def initialize_database():
    """
    Erstellt die erforderlichen Tabellen in der Datenbank, falls diese nicht existieren.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                rsi REAL NOT NULL,
                signal TEXT NOT NULL,
                action TEXT NOT NULL,
                last_price REAL,
                trade_fee REAL,
                timestamp INTEGER,
                profit REAL,
                price_change REAL,
                volume REAL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL UNIQUE,
                active INTEGER DEFAULT 1
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS training_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp INTEGER NOT NULL,
                pair TEXT NOT NULL,
                rsi REAL NOT NULL,
                profit REAL,
                price_change REAL,
                volume REAL
            )
        """)
        conn.commit()
        conn.close()
        logging.info("Datenbank und Tabellen initialisiert.")
    except Exception as e:
        logging.error(f"Fehler bei der Initialisierung der Datenbank: {e}")

def initialize_pairs_table(exchange):
    """
    Initialisiert die Tabelle 'pairs' mit verfügbaren Handelspaaren von der Binance-API.
    :param exchange: Das Exchange-Objekt für die Binance-Verbindung.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Märkte von Binance abrufen
        markets = exchange.load_markets()
        pairs = list(markets.keys())

        # Paare in die Datenbank einfügen
        for pair in pairs:
            cursor.execute("""
                INSERT OR IGNORE INTO pairs (pair, active)
                VALUES (?, 1)
            """, (pair,))

        conn.commit()
        conn.close()
        logging.info(f"{len(pairs)} Handelspaare erfolgreich in die Tabelle 'pairs' eingefügt.")
    except Exception as e:
        logging.error(f"Fehler beim Initialisieren der 'pairs'-Tabelle: {e}")

def log_to_db(pair, rsi, signal, action, last_price=None, trade_fee=None, timestamp=None, profit=None, price_change=None, volume=None):
    """
    Loggt Handelssignale in die Datenbank.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO trades (pair, rsi, signal, action, last_price, trade_fee, timestamp, profit, price_change, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (pair, rsi, signal, action, last_price, trade_fee, timestamp, profit, price_change, volume))
        conn.commit()
        conn.close()
        logging.info(f"Handelssignal für {pair} in die Datenbank geschrieben.")
    except Exception as e:
        logging.error(f"Fehler beim Schreiben in die Datenbank: {e}")

def load_active_pairs():
    """
    Lädt aktive Handelspaare aus der Datenbank.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT pair FROM pairs WHERE active = 1")
        pairs = [row[0] for row in cursor.fetchall()]
        conn.close()
        return pairs
    except Exception as e:
        logging.error(f"Fehler beim Laden der Handelspaare: {e}")
        return []

def add_pair(pair):
    """
    Fügt ein neues Handelspaar in die Datenbank hinzu.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO pairs (pair) VALUES (?)
        """, (pair,))
        conn.commit()
        conn.close()
        logging.info(f"Handelspaar {pair} hinzugefügt.")
    except Exception as e:
        logging.error(f"Fehler beim Hinzufügen des Handelspaares {pair}: {e}")

def deactivate_pair(pair):
    """
    Setzt ein Handelspaar auf inaktiv.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE pairs SET active = 0 WHERE pair = ?
        """, (pair,))
        conn.commit()
        conn.close()
        logging.info(f"Handelspaar {pair} deaktiviert.")
    except Exception as e:
        logging.error(f"Fehler beim Deaktivieren des Handelspaares {pair}: {e}")

def populate_training_data():
    """
    Füllt die training_data-Tabelle mit Werten aus der trades-Tabelle.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO training_data (timestamp, pair, rsi, profit, price_change, volume)
            SELECT timestamp, pair, rsi, profit, price_change, volume
            FROM trades
            WHERE profit IS NOT NULL
        """)
        conn.commit()
        count = cursor.rowcount
        conn.close()
        logging.info(f"{count} Datensätze erfolgreich in training_data eingefügt.")
    except Exception as e:
        logging.error(f"Fehler beim Einfügen von Daten in training_data: {e}")
