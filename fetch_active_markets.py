import sqlite3

def get_active_spot_markets(db_path='trading_data.db'):
    """
    Lade alle aktiven Spot-Märkte aus der Datenbank.
    
    :param db_path: Pfad zur SQLite-Datenbank.
    :return: Liste der relevanten Märkte.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = '''
        SELECT symbol, base_asset, quote_asset, maker_fee, taker_fee
        FROM binance_markets
        WHERE is_active = 1 AND market_type = 'spot';
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"{len(results)} aktive Spot-Märkte gefunden.")
        return results
    except Exception as e:
        print(f"Fehler beim Abrufen der Märkte: {str(e)}")
        return []
    finally:
        conn.close()

if __name__ == "__main__":
    # Relevante Märkte abrufen
    active_markets = get_active_spot_markets()
    print(f"Gefundene Märkte: {len(active_markets)}")
    if active_markets:
        print("Beispiele:")
        for market in active_markets[:10]:
            print(market)
