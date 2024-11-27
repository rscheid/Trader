import sqlite3

# Verbindung zur Datenbank herstellen
db_path = "trading_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Spalten zur Tabelle hinzufügen (falls nicht existierend)
try:
    cursor.execute("ALTER TABLE binance_markets ADD COLUMN maker_fee REAL DEFAULT 0.001")
    cursor.execute("ALTER TABLE binance_markets ADD COLUMN taker_fee REAL DEFAULT 0.001")
    print("Spalten 'maker_fee' und 'taker_fee' erfolgreich hinzugefügt.")
except sqlite3.OperationalError as e:
    print(f"Spalten konnten nicht hinzugefügt werden (vielleicht existieren sie bereits): {str(e)}")

conn.commit()
conn.close()
