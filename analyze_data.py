import sqlite3
import pandas as pd

def analyze_table(table_name, db_name='trading_data.db'):
    """
    Analyse einer einzelnen Tabelle: Grundlegende Statistiken und fehlende Werte.
    """
    conn = sqlite3.connect(db_name)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()

    # Grundlegende Statistiken
    print(f"--- Analyse für {table_name} ---")
    print(df.describe())

    # Prüfen auf fehlende Werte
    missing_values = df.isnull().sum()
    print("\nFehlende Werte:")
    print(missing_values)

    # Verteilung des Volumens
    print("\nVolumen-Statistik:")
    print(df['volume'].describe())

def analyze_all_tables(db_name='trading_data.db'):
    """
    Analyse aller Tabellen in der Datenbank.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    for table in tables:
        analyze_table(table, db_name)

if __name__ == "__main__":
    analyze_all_tables()
