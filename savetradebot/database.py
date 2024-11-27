import sqlite3
import logging
import os

# Datenbankpfad
DB_PATH = "trading_data.db"

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def initialize_database():
    """
    Erstellt die erforderlichen Tabellen in der Datenbank, falls diese nicht existieren.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Tabelle 'trades' erstellen
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL,
                rsi REAL,
                signal TEXT,
                action TEXT,
                last_price REAL,
                trade_fee REAL,
                price_change REAL,
                volume REAL,
                open_price REAL,
                high_price REAL,
                low_price REAL,
                close_time INTEGER,
                profit REAL,
                timestamp INTEGER
            )
        """)

        # Tabelle 'pairs' erstellen
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pairs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pair TEXT NOT NULL UNIQUE,
                active INTEGER DEFAULT 1
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

def log_to_db(pair, rsi, signal, action, last_price=None, trade_fee=None, price_change=None, volume=None, timestamp=None, profit=None):
    """
    Loggt Handelssignale in die Datenbank.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Standardwerte setzen
        last_price = last_price or 0.0
        trade_fee = trade_fee or 0.0
        price_change = price_change or 0.0
        volume = volume or 0.0
        timestamp = timestamp or int(time.time())
        profit = profit or 0.0

        # Daten einfügen
        cursor.execute("""
            INSERT INTO trades (pair, rsi, signal, action, last_price, trade_fee, price_change, volume, timestamp, profit)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (pair, rsi, signal, action, last_price, trade_fee, price_change, volume, timestamp, profit))

        conn.commit()
        conn.close()
        logging.info(f"Handelssignal für {pair} erfolgreich in die Datenbank geschrieben.")
    except Exception as e:
        logging.error(f"Fehler beim Schreiben in die Datenbank: {e}", exc_info=True)

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

if __name__ == "__main__":
    # Initialisierung der Datenbank und Tabellen
    initialize_database()

    # Beispiel-Testdaten in die Tabelle 'trades' schreiben
    log_to_db(
        pair="BTC/USDT",
        rsi=45.67,
        signal="HOLD",
        action="Kein Trade",
        last_price=45000,
        trade_fee=45,
        price_change=100,
        volume=5000,
        timestamp=1234567890,
        profit=0.0
    )
    logging.info("Testdaten erfolgreich hinzugefügt.")
