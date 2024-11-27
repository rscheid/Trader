import sqlite3
import ccxt

# Verbindung zur Datenbank herstellen
db_path = "trading_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Tabelle erstellen, falls sie noch nicht existiert
cursor.execute('''
    CREATE TABLE IF NOT EXISTS binance_markets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT UNIQUE NOT NULL,
        base_asset TEXT NOT NULL,
        quote_asset TEXT NOT NULL,
        active INTEGER NOT NULL,
        market_type TEXT NOT NULL,
        tick_size REAL NOT NULL,
        min_qty REAL NOT NULL,
        max_qty REAL NOT NULL,
        step_size REAL NOT NULL,
        maker_fee REAL DEFAULT 0.001,
        taker_fee REAL DEFAULT 0.001
    )
''')
conn.commit()

# Binance-Märkte abrufen und speichern
def fetch_and_store_markets():
    try:
        exchange = ccxt.binance()
        markets = exchange.load_markets()
        print(f"{len(markets)} Märkte geladen.")

        for market_symbol, market_data in markets.items():
            cursor.execute('''
                INSERT OR IGNORE INTO binance_markets (
                    symbol, base_asset, quote_asset, active, market_type,
                    tick_size, min_qty, max_qty, step_size, maker_fee, taker_fee
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                market_symbol,
                market_data['base'],
                market_data['quote'],
                1 if market_data['active'] else 0,
                market_data.get('type', 'spot'),
                market_data['precision']['price'],
                market_data['limits']['amount']['min'],
                market_data['limits']['amount']['max'],
                market_data['precision']['amount'],
                market_data.get('maker', 0.001),  # Standardgebühr, falls nicht verfügbar
                market_data.get('taker', 0.001)   # Standardgebühr, falls nicht verfügbar
            ))
        conn.commit()
        print(f"{len(markets)} Märkte erfolgreich in die Tabelle 'binance_markets' eingefügt.")
    except Exception as e:
        print(f"Fehler beim Abrufen und Speichern der Märkte: {str(e)}")
    finally:
        conn.close()

# Märkte abrufen und speichern
fetch_and_store_markets()
