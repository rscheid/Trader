import ccxt

def fetch_trading_pairs():
    """Alle verfügbaren Handelspaare von Binance abrufen."""
    exchange = ccxt.binance()
    markets = exchange.load_markets()
    trading_pairs = [market for market in markets]
    return trading_pairs

if __name__ == "__main__":
    pairs = fetch_trading_pairs()
    print(f"Gefundene Handelspaare: {len(pairs)}")
    print("Beispiele:", pairs[:10])
