import sqlite3

def get_active_spot_markets(db_path='trading_data.db', min_volume=1000000, min_volatility=0.01):
    """
    Lade alle aktiven Spot-Märkte aus der Datenbank mit zusätzlichen Filtern.

    :param db_path: Pfad zur SQLite-Datenbank.
    :param min_volume: Mindestvolumen der letzten 24 Stunden.
    :param min_volatility: Minimale Volatilität der letzten 24 Stunden.
    :return: Liste der relevanten Märkte.
    """
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = f'''
        SELECT symbol, base AS base_asset, quote AS quote_asset, maker AS maker_fee, taker AS taker_fee
        FROM binance_markets
        WHERE is_active = 1
          AND market_type = 'spot'
          AND volume_24h > {min_volume}
          AND volatility_24h > {min_volatility};
        '''
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"{len(results)} relevante Spot-Märkte gefunden.")
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
