import random
import numpy as np

def fetch_candles(pair):
    """
    Simuliert das Abrufen von Candle-Daten.
    :param pair: Handelspaar
    :return: Liste von Candle-Daten
    """
    # Simulierte Kerzendaten: [timestamp, open, high, low, close, volume]
    candles = [[i, random.uniform(0.8, 1.2), random.uniform(0.9, 1.3), random.uniform(0.7, 1.1), random.uniform(0.8, 1.2), random.uniform(10, 100)] for i in range(14)]
    return candles

def calculate_rsi(prices, period=14):
    """
    Berechnet den RSI (Relative Strength Index).
    :param prices: Liste der Schlusskurse
    :param period: Periode für RSI
    :return: RSI-Wert
    """
    if len(prices) < period:
        return None

    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_profit(last_price, fee_percent, signal):
    """
    Berechnet den erwarteten Profit eines Trades.
    :param last_price: Letzter Preis
    :param fee_percent: Gebührenrate
    :param signal: "BUY" oder "SELL"
    :return: Erwarteter Profit
    """
    # Beispielhafte Berechnung (Trade-Logik kann angepasst werden)
    trade_fee = last_price * fee_percent
    if signal == "BUY":
        # Kauf simuliert; kein Gewinn bis zum Verkauf
        return -trade_fee
    elif signal == "SELL":
        # Verkauf simuliert; einfacher Gewinn
        return last_price - trade_fee
    else:
        return 0

def update_ki_model(model, pair, rsi, signal, profit):
    """
    Aktualisiert das KI-Modell basierend auf den neuesten Trades.
    :param model: LSTM-Modell (Platzhalter)
    :param pair: Handelspaar
    :param rsi: RSI-Wert
    :param signal: Signal ("BUY", "SELL", "HOLD")
    :param profit: Erzielter Profit
    """
    # Platzhalter für KI-Modell-Training
    print(f"Trainiere KI mit Daten: {pair}, RSI: {rsi}, Signal: {signal}, Profit: {profit}")
