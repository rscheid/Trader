import ccxt

def analyze_binance_schema():
    exchange = ccxt.binance()
    markets = exchange.load_markets()
    print(f"Anzahl Märkte: {len(markets)}")

    # Ins erste Marktobjekt schauen
    example_market = next(iter(markets.values()))
    print("Beispieldaten eines Marktes:")
    for key, value in example_market.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    analyze_binance_schema()
