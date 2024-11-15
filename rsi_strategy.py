import ccxt

# Binance API-Konfiguration
API_KEY = "YOUR_TESTNET_API_KEY"
SECRET_KEY = "YOUR_TESTNET_SECRET"

# Verbindung zur Binance-Testnet-API herstellen
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
    'enableRateLimit': True,
})

# Testnet aktivieren
exchange.set_sandbox_mode(True)

def calculate_rsi(closes):
    """Berechnet den RSI basierend auf Schlusskursen."""
    gains = [closes[i] - closes[i-1] for i in range(1, len(closes)) if closes[i] > closes[i-1]]
    losses = [closes[i-1] - closes[i] for i in range(1, len(closes)) if closes[i] < closes[i-1]]

    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 1  # Kein Verlust = künstlich 1

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_rsi_signal(symbol="BTC/USDT", timeframe='1m', limit=14):
    """Holt Marktdaten, berechnet den RSI und gibt ein Signal zurück."""
    try:
        # Hole historische Marktdaten
        candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        closes = [c[4] for c in candles]  # Nur Schlusskurse

        # Berechne den RSI
        rsi = calculate_rsi(closes)

        # Entscheidungslogik basierend auf dem RSI
        if rsi < 30:
            return f"BUY Signal: RSI={rsi:.2f}"
        elif rsi > 70:
            return f"SELL Signal: RSI={rsi:.2f}"
        else:
            return f"HOLD Signal: RSI={rsi:.2f}"
    except Exception as e:
        return f"Error in get_rsi_signal: {e}"

# Testlauf
if __name__ == "__main__":
    print(get_rsi_signal())
