import sqlite3

def store_to_sqlite(df, table_name, db_name='trading_data.db'):
    """
    Speichert die Daten in einer SQLite-Datenbank.
    """
    try:
        conn = sqlite3.connect(db_name)
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        print(f"Daten für {table_name} erfolgreich gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Daten in {table_name}: {e}")

if __name__ == "__main__":
    from fetch_historical import fetch_historical_data

    # Beispiel: BTC/USDT
    pair = 'BTC/USDT'
    table_name = pair.replace('/', '_')  # Ersetze "/" durch "_"
    data = fetch_historical_data(pair)

    if data is not None:
        store_to_sqlite(data, table_name)
