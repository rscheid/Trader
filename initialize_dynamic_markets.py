import sqlite3
import ccxt


def initialize_dynamic_table():
    """Initialisiert oder erstellt die Tabelle 'binance_markets' basierend auf den API-Daten von Binance."""
    try:
        # Verbindung zur SQLite-Datenbank herstellen
        conn = sqlite3.connect("trading_data.db")
        cursor = conn.cursor()

        # Binance-API verwenden, um Märkte abzurufen
        print("Verbinde zur Binance-API...")
        exchange = ccxt.binance()
        markets = exchange.load_markets()
        print(f"{len(markets)} Märkte erfolgreich abgerufen.")

        # Beispiel-Marktdaten abrufen
        example_market = next(iter(markets.values()))
        print("Schema wird analysiert...")

        # Dynamisches Schema erstellen
        columns = {
            "symbol": "TEXT UNIQUE NOT NULL",
            "base_asset": "TEXT",
            "quote_asset": "TEXT",
            "is_active": "INTEGER",
            "market_type": "TEXT",
        }

        # Zusätzliche Felder aus den API-Daten hinzufügen
        for key, value in example_market.items():
            if isinstance(value, (int, float)):
                columns[key] = "REAL"
            elif isinstance(value, str):
                columns[key] = "TEXT"
            elif isinstance(value, bool):
                columns[key] = "INTEGER"

        # Tabelle erstellen, falls sie nicht existiert
        print("Tabelle 'binance_markets' wird erstellt...")
        create_table_sql = f'''
        CREATE TABLE IF NOT EXISTS binance_markets (
            {", ".join([f"{col} {dtype}" for col, dtype in columns.items()])}
        );
        '''
        cursor.execute(create_table_sql)

        # Bestehendes Schema prüfen
        cursor.execute("PRAGMA table_info(binance_markets);")
        existing_columns = {row[1]: row[2] for row in cursor.fetchall()}

        # Fehlende Spalten hinzufügen
        for col_name, col_type in columns.items():
            if col_name not in existing_columns:
                cursor.execute(f"ALTER TABLE binance_markets ADD COLUMN {col_name} {col_type}")
                print(f"Spalte '{col_name}' hinzugefügt.")

        # Daten in die Tabelle einfügen
        print("Daten werden eingefügt...")
        for market_id, market_data in markets.items():
            market_data["symbol"] = market_id
            market_data["base_asset"] = market_data.get("base", "")
            market_data["quote_asset"] = market_data.get("quote", "")
            market_data["is_active"] = int(market_data.get("active", False))
            market_data["market_type"] = market_data.get("type", "")

            # Dynamische Werte setzen mit Typ-Validierung
            values = {}
            for col in columns.keys():
                value = market_data.get(col, None)
                if value is None:
                    values[col] = None
                elif columns[col] == "REAL" and not isinstance(value, (int, float)):
                    try:
                        values[col] = float(value)
                    except ValueError:
                        values[col] = None
                elif columns[col] == "INTEGER" and not isinstance(value, int):
                    try:
                        values[col] = int(value)
                    except ValueError:
                        values[col] = None
                elif columns[col] == "TEXT" and not isinstance(value, str):
                    values[col] = str(value)
                else:
                    values[col] = value

            placeholders = ", ".join([":" + col for col in columns.keys()])
            insert_sql = f'''
            INSERT OR REPLACE INTO binance_markets ({", ".join(columns.keys())})
            VALUES ({placeholders});
            '''
            cursor.execute(insert_sql, values)

        # Änderungen speichern
        conn.commit()
        print("Daten erfolgreich eingefügt.")

    except sqlite3.OperationalError as e:
        print(f"Fehler beim Erstellen oder Einfügen der Tabelle: {e}")
    except ccxt.BaseError as e:
        print(f"Fehler bei der Binance-API-Kommunikation: {e}")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    initialize_dynamic_table()
