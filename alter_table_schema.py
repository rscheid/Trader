import sqlite3

db_path = "trading_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

def alter_table_to_match_schema():
    required_columns = {
        "is_active": "INTEGER",
        "market_type": "TEXT",
    }

    # Prüfe vorhandene Spalten
    cursor.execute("PRAGMA table_info(binance_markets);")
    existing_columns = {col[1]: col[2] for col in cursor.fetchall()}

    # Fehlende Spalten hinzufügen
    for column, column_type in required_columns.items():
        if column not in existing_columns:
            print(f"Füge Spalte {column} ({column_type}) hinzu...")
            cursor.execute(f"ALTER TABLE binance_markets ADD COLUMN {column} {column_type};")
            conn.commit()

if __name__ == "__main__":
    alter_table_to_match_schema()
    print("Schema erfolgreich angepasst.")
    conn.close()
