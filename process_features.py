import pandas as pd
import numpy as np

# Funktionen zur Berechnung der Features
def calculate_ask_bid_spread(ask_prices, bid_prices):
    return (ask_prices - bid_prices) / ((ask_prices + bid_prices) / 2)

def calculate_relative_price_change(prices, window=5):
    return prices.pct_change(periods=window)

def calculate_volume_ratio(buy_volume, sell_volume):
    return buy_volume / (sell_volume + 1e-8)

def calculate_volatility_cluster(prices, window=10):
    return prices.rolling(window=window).std()

def calculate_rsi(prices, window=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

# Hauptfunktion zur Feature-Berechnung
def add_features(df):
    if "AskPrice" in df.columns and "BidPrice" in df.columns:
        df["AskBidSpread"] = calculate_ask_bid_spread(df["AskPrice"], df["BidPrice"])
    else:
        df["AskBidSpread"] = 0  # Platzhalter

    df["RelativePriceChange"] = calculate_relative_price_change(df["Price"], window=5)

    if "BuyVolume" in df.columns and "SellVolume" in df.columns:
        df["VolumeRatio"] = calculate_volume_ratio(df["BuyVolume"], df["SellVolume"])
    else:
        df["VolumeRatio"] = 0  # Platzhalter

    df["RSI_Short"] = calculate_rsi(df["Price"], window=14)
    df["RSI_Long"] = calculate_rsi(df["Price"], window=50)

    df["VolatilityCluster"] = calculate_volatility_cluster(df["Price"], window=10)

    df = df.fillna(0)
    return df

# Laden der aktuellen Daten
def load_and_process_data(log_file="trade_log.csv"):
    # Annahme: Deine Datei enthält die folgenden Spalten
    columns = ["Action", "Price", "Mu", "Sigma", "SimulationResult", "ActualPriceAfterTrade"]
    df = pd.read_csv(log_file, names=columns)

    # Falls weitere Spalten fehlen, generiere Dummy-Werte
    if "AskPrice" not in df.columns:
        df["AskPrice"] = df["Price"] * 1.01  # Dummy: 1% höher als Preis
    if "BidPrice" not in df.columns:
        df["BidPrice"] = df["Price"] * 0.99  # Dummy: 1% niedriger als Preis
    if "BuyVolume" not in df.columns:
        df["BuyVolume"] = np.random.uniform(50, 100, size=len(df))  # Dummy-Werte
    if "SellVolume" not in df.columns:
        df["SellVolume"] = np.random.uniform(40, 90, size=len(df))  # Dummy-Werte

    # Features hinzufügen
    df = add_features(df)
    return df

# Teste den Prozess
if __name__ == "__main__":
    df = load_and_process_data()
    print("--- Erweiterte Daten mit Features ---")
    print(df.head())
    df.to_csv("trade_log_with_features.csv", index=False)
    print("\nErweiterte Daten wurden in 'trade_log_with_features.csv' gespeichert.")
