from binance_api import setup_exchange

# Deine API-Schlüssel hier einfügen
API_KEY = "dein_api_key"  # Ersetze durch deinen Testnetz-API-Schlüssel
SECRET_KEY = "dein_secret_key"  # Ersetze durch deinen Testnetz-Secret-Schlüssel

# Testnetz aktivieren
exchange = setup_exchange(API_KEY, SECRET_KEY, testnet=True)

try:
    print("Verbindung wird getestet...")
    
    # Test: Märkte laden
    print("Lade Märkte...")
    markets = exchange.load_markets()
    print(f"Märkte erfolgreich geladen: {len(markets)}")

    # Test: Abruf von Kerzendaten
    print("Teste Abruf von Kerzendaten für BTC/USDT...")
    candles = exchange.fetch_ohlcv('BTC/USDT', timeframe='1m', limit=5)
    print("Kerzendaten erfolgreich abgerufen:")
    for candle in candles:
        print(candle)
except Exception as e:
    print("Fehler beim Testen der Verbindung:", str(e))
