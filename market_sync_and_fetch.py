import sqlite3
import ccxt
import logging
from datetime import datetime

def sync_and_fetch():
    try:
        logging.info("Verbinde zur Binance-API...")
        exchange = ccxt.binance()
        markets = exchange.load_markets()
        logging.info(f"{len(markets)} Märkte erfolgreich abgerufen.")
        # Hier können weitere Verarbeitungsschritte erfolgen, z. B. Datenbankupdates
    except Exception as e:
        logging.error(f"Fehler bei der Synchronisierung: {e}")
        raise  # Fehler weitergeben, damit der Main-Loop ihn erkennt


DB_FILE = "trading_data.db"
SYNC_INTERVAL = 300  # Sekunden (5 Minuten)


def log(message):
    """Protokolliert eine Nachricht mit Zeitstempel."""
    timestamp = datetime.now().isoformat()
    print(f"[{timestamp}] {message}")


def initialize_table():
    """Initialisiert die Tabelle `binance_markets` mit einem eindeutigen Schema."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Tabelle erstellen oder bestehende Struktur prüfen
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS binance_markets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT UNIQUE NOT NULL,
                base TEXT NOT NULL,
                quote TEXT NOT NULL,
                is_active INTEGER NOT NULL,
                market_type TEXT NOT NULL,
                baseId TEXT,
                quoteId TEXT,
                type TEXT,
                spot INTEGER,
                margin INTEGER,
                swap INTEGER,
                future INTEGER,
                option INTEGER,
                contract INTEGER,
                taker REAL,
                maker REAL,
                tierBased INTEGER,
                percentage INTEGER,
                feeSide TEXT
            )
        ''')
        conn.commit()
        log("Tabelle `binance_markets` initialisiert.")
    except sqlite3.Error as e:
        log(f"Fehler beim Initialisieren der Tabelle: {e}")
    finally:
        conn.close()


def update_markets():
    """Aktualisiert die Handelspaare in der Datenbank mit den neuesten Daten von Binance."""
    try:
        # Verbindung zur Binance-API
        exchange = ccxt.binance()
        log("Lade Märkte von Binance...")
        markets = exchange.load_markets()

        # Verbindung zur Datenbank
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Datenbankeinträge aktualisieren
        for symbol, market in markets.items():
            data = {
                "symbol": market.get("symbol"),
                "base": market.get("base", ""),
                "quote": market.get("quote", ""),
                "is_active": int(market.get("active", 1)),
                "market_type": market.get("type", ""),
                "baseId": market.get("baseId", ""),
                "quoteId": market.get("quoteId", ""),
                "type": market.get("type", ""),
                "spot": int(market.get("spot", 0)),
                "margin": int(market.get("margin", 0)),
                "swap": int(market.get("swap", 0)),
                "future": int(market.get("future", 0)),
                "option": int(market.get("option", 0)),
                "contract": int(market.get("contract", 0)),
                "taker": float(market.get("taker", 0.001)),
                "maker": float(market.get("maker", 0.001)),
                "tierBased": int(market.get("tierBased", 0)),
                "percentage": int(market.get("percentage", 0)),
                "feeSide": market.get("feeSide", ""),
            }

            cursor.execute('''
                INSERT INTO binance_markets (
                    symbol, base, quote, is_active, market_type,
                    baseId, quoteId, type, spot, margin, swap, future, option, contract,
                    taker, maker, tierBased, percentage, feeSide
                )
                VALUES (
                    :symbol, :base, :quote, :is_active, :market_type,
                    :baseId, :quoteId, :type, :spot, :margin, :swap, :future, :option, :contract,
                    :taker, :maker, :tierBased, :percentage, :feeSide
                )
                ON CONFLICT(symbol) DO UPDATE SET
                    base = excluded.base,
                    quote = excluded.quote,
                    is_active = excluded.is_active,
                    market_type = excluded.market_type,
                    baseId = excluded.baseId,
                    quoteId = excluded.quoteId,
                    type = excluded.type,
                    spot = excluded.spot,
                    margin = excluded.margin,
                    swap = excluded.swap,
                    future = excluded.future,
                    option = excluded.option,
                    contract = excluded.contract,
                    taker = excluded.taker,
                    maker = excluded.maker,
                    tierBased = excluded.tierBased,
                    percentage = excluded.percentage,
                    feeSide = excluded.feeSide
            ''', data)

        conn.commit()
        log(f"{len(markets)} Märkte erfolgreich aktualisiert.")
    except sqlite3.Error as e:
        log(f"Fehler beim Aktualisieren der Märkte in der Datenbank: {e}")
    except Exception as e:
        log(f"Allgemeiner Fehler beim Abrufen oder Speichern der Märkte: {e}")
    finally:
        conn.close()


def main():
    """Hauptprozess für die zyklische Aktualisierung."""
    initialize_table()

    while True:
        log("Aktualisiere Handelspaare...")
        try:
            update_markets()
        except Exception as e:
            log(f"Fehler in der Hauptschleife: {e}")

        log("Warte 5 Minuten...")
        time.sleep(SYNC_INTERVAL)


if __name__ == "__main__":
    main()
