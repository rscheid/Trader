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

def fetch_candles(exchange, symbol, timeframe="1m", limit=5):
    """
    Ruft Kerzendaten von Binance ab.
    :param exchange: Binance-Exchange-Objekt
    :param symbol: Handelspaar (z.B. BTC/USDT)
    :param timeframe: Zeitrahmen (z.B. 1m, 5m, 1h)
    :param limit: Anzahl der Kerzen
    :return: Liste der Kerzendaten
    """
    try:
        return exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    except Exception as e:
        raise RuntimeError(f"Fehler beim Abrufen von Kerzendaten für {symbol}: {e}")
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

def fetch_candles(exchange, symbol, timeframe="1m", limit=5):
    """
    Ruft Kerzendaten von Binance ab.
    :param exchange: Binance-Exchange-Objekt
    :param symbol: Handelspaar (z.B. BTC/USDT)
    :param timeframe: Zeitrahmen (z.B. 1m, 5m, 1h)
    :param limit: Anzahl der Kerzen
    :return: Liste der Kerzendaten
    """
    try:
        return exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    except Exception as e:
        raise RuntimeError(f"Fehler beim Abrufen von Kerzendaten für {symbol}: {e}")
