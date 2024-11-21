import sqlite3
import pandas as pd
from database import save_symbols_to_db

def rank_all_tables(db_name="trading_data.db"):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    results = []
    for table in tables:
        if table in ["active_pairs", "trading_data"]:
            continue

        # Analysiere die Tabelle
        df = pd.read_sql(f"SELECT * FROM {table}", conn)
        avg_volume = df["volume"].mean()
        stability = ((df["high"] - df["low"]) / df["close"]).mean()
        results.append({"pair": table, "avg_volume": avg_volume, "stability": stability})

    df_results = pd.DataFrame(results)
    df_results = df_results.sort_values(by=["avg_volume", "stability"], ascending=[False, True])

    # Top-Paare auswählen und speichern
    top_pairs = df_results["pair"].head(50).tolist()
    save_symbols_to_db(top_pairs)
    logging.info("Top 50 Paare in active_pairs gespeichert.")

if __name__ == "__main__":
    rank_all_tables()

