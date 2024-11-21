import ccxt

def setup_exchange(api_key, secret_key, testnet=False):
    """
    Initialisiert die Binance-Exchange-Verbindung.
    :param api_key: API-Schlüssel
    :param secret_key: Secret-Schlüssel
    :param testnet: Boolean, ob Testnet verwendet werden soll
    :return: Binance Exchange-Objekt
    """
    try:
        exchange = ccxt.binance({
            'apiKey': api_key,
            'secret': secret_key,
            'options': {
                'defaultType': 'spot',
            },
        })
        if testnet:
            exchange.set_sandbox_mode(True)
            exchange.urls['api'] = exchange.urls['test']
        return exchange
    except Exception as e:
        raise RuntimeError(f"Fehler beim Einrichten der Binance-Verbindung: {e}")

def fetch_candles(exchange, pair, timeframe="1m", limit=14):
    """
    Holt Candle-Daten für ein bestimmtes Handelspaar.
    :param exchange: Binance-Exchange-Objekt
    :param pair: Handelspaar (z.B. "BTC/USDT")
    :param timeframe: Zeitrahmen (z.B. "1m", "5m")
    :param limit: Anzahl der Kerzen
    :return: Liste von OHLCV-Daten
    """
    try:
        candles = exchange.fetch_ohlcv(pair, timeframe=timeframe, limit=limit)
        return candles
    except Exception as e:
        raise RuntimeError(f"Fehler beim Abrufen von Kerzendaten für {pair}: {e}")
