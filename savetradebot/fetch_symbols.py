import ccxt
import sqlite3

def fetch_binance_symbols():
    try:
        exchange = ccxt.binance()
        markets = exchange.load_markets()
        symbols = list(markets.keys())
        print(f"Erfolgreich {len(symbols)} Handelspaare geladen.")
        return symbols
    except Exception as e:
        print(f"Fehler beim Laden der Handelspaare: {str(e)}")
        return []


def save_symbols_to_db(symbols):
    try:
        conn = sqlite3.connect('trading_data.db')  # Verbindung zur Datenbank
        cursor = conn.cursor()

        # Tabelle erstellen, falls nicht existiert
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS active_pairs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT UNIQUE NOT NULL
        )
        ''')

        # Symbole einfügen
        for symbol in symbols:
            try:
                cursor.execute('INSERT OR IGNORE INTO active_pairs (symbol) VALUES (?)', (symbol,))
            except Exception as e:
                print(f"Fehler beim Einfügen von {symbol}: {str(e)}")

        conn.commit()
        print(f"{len(symbols)} Symbole erfolgreich gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern in die Datenbank: {str(e)}")
    finally:
        conn.close()

# Testlauf
if __name__ == "__main__":
    handelspaare = fetch_binance_symbols()
    save_symbols_to_db(handelspaare)


