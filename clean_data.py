import sqlite3
import pandas as pd

def clean_table(table_name, db_name='trading_data.db'):
    """
    Bereinigt eine Tabelle: Entfernt illiquide Perioden und Ausreißer.
    """
    conn = sqlite3.connect(db_name)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)

    # Filter: Entferne Zeilen mit 0-Volumen
    initial_count = len(df)
    df = df[df['volume'] > 0]

    # Filter: Entferne extreme Ausreißer (z. B. über dem 99. Perzentil)
    volume_99th = df['volume'].quantile(0.99)
    df = df[df['volume'] <= volume_99th]

    # Überprüfen, ob Tabelle leer ist
    if len(df) == 0:
        print(f"{table_name}: Nach Bereinigung keine Daten übrig.")
        conn.close()
        return

    # Aktualisierte Tabelle speichern
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
    print(f"{table_name}: Bereinigt und gespeichert ({len(df)} von {initial_count} Einträgen behalten).")

def clean_all_tables(db_name='trading_data.db'):
    """
    Bereinigt alle Tabellen in der Datenbank.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    for table in tables:
        clean_table(table, db_name)

if __name__ == "__main__":
    clean_all_tables()
