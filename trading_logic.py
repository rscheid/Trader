import ccxt
import logging

# Binance Testnet konfigurieren
def setup_exchange(api_key, secret_key):
    exchange = ccxt.binance({
        'apiKey': api_key,
        'secret': secret_key,
        'enableRateLimit': True,
    })
    exchange.set_sandbox_mode(True)
    return exchange

def calculate_rsi(closes, period=14):
    delta = [closes[i] - closes[i - 1] for i in range(1, len(closes))]
    gains = [d for d in delta if d > 0]
    losses = [-d for d in delta if d < 0]

    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 1  # Kein Verlust = künstlich 1

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
