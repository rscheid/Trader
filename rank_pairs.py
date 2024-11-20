import sqlite3
import pandas as pd

def analyze_table(table_name, db_name='trading_data.db'):
    """
    Analyse einzelner Tabellen, um Liquidität und Preisstabilität zu bewerten.
    """
    conn = sqlite3.connect(db_name)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    conn.close()

    # Durchschnittliches Volumen und Preisstabilität berechnen
    avg_volume = df['volume'].mean()
    price_stability = ((df['high'] - df['low']) / df['close']).mean()

    return {
        'pair': table_name,
        'avg_volume': avg_volume,
        'price_stability': price_stability,
        'rows': len(df)  # Anzahl der verbleibenden Datenpunkte
    }

def rank_all_tables(db_name='trading_data.db'):
    """
    Bewertet alle Tabellen und sortiert sie nach Liquidität und Stabilität.
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    results = []
    for table in tables:
        result = analyze_table(table, db_name)
        results.append(result)

    # Ergebnisse sortieren: Zuerst nach Volumen, dann nach Stabilität
    results = sorted(results, key=lambda x: (-x['avg_volume'], x['price_stability']))

    return pd.DataFrame(results)

if __name__ == "__main__":
    results_df = rank_all_tables()
    print(results_df)

    # Ergebnisse speichern
    results_df.to_csv('pair_rankings.csv', index=False)
    print("Ergebnisse gespeichert in 'pair_rankings.csv'")
