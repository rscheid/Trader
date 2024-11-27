import sqlite3
import pandas as pd

def calculate_fees(df, fee_rate=0.001):
    """
    Gebühren berechnen und Daten erweitern.
    """
    df['fees'] = df['close'] * df['volume'] * fee_rate
    df['net_volume'] = df['volume'] - df['fees']
    return df

def update_database_with_fees(pair, db_name='trading_data.db'):
    """
    Holt Daten aus der Datenbank, berechnet Gebühren und speichert sie zurück.
    """
    table_name = pair.replace('/', '_')
    
    try:
        # Verbindung zur Datenbank herstellen
        conn = sqlite3.connect(db_name)

        # Daten abrufen
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        
        # Gebühren berechnen
        df = calculate_fees(df)
        
        # Tabelle aktualisieren
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        conn.close()
        print(f"Gebühren für {pair} erfolgreich berechnet und gespeichert.")
    except Exception as e:
        print(f"Fehler bei der Aktualisierung der Tabelle {table_name}: {e}")

if __name__ == "__main__":
    # Beispiel: BTC/USDT
    pair = 'BTC/USDT'
    update_database_with_fees(pair)
