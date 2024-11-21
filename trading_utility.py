import random
import numpy as np
import logging

def fetch_candles(pair):
    """
    Simuliert das Abrufen von Candle-Daten.
    :param pair: Handelspaar
    :return: Liste von Candle-Daten
    """
    # Simulierte Kerzendaten: [timestamp, open, high, low, close, volume]
    candles = [[i, random.uniform(0.8, 1.2), random.uniform(0.9, 1.3), random.uniform(0.7, 1.1), random.uniform(0.8, 1.2), random.uniform(10, 100)] for i in range(14)]
    logging.debug(f"{pair} - Simulierte Kerzendaten: {candles[:5]}")  # Logge die ersten 5 Einträge
    return candles

def calculate_rsi(prices, period=14):
    """
    Berechnet den RSI (Relative Strength Index).
    :param prices: Liste der Schlusskurse
    :param period: Periode für RSI
    :return: RSI-Wert
    """
    if len(prices) < period:
        logging.warning("Zu wenige Datenpunkte für RSI-Berechnung.")
        return None

    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    logging.debug(f"RSI berechnet: {rsi:.2f}")
    return rsi

def calculate_profit(last_price, fee_percent, signal):
    """
    Berechnet den erwarteten Profit eines Trades.
    :param last_price: Letzter Preis
    :param fee_percent: Gebührenrate
    :param signal: "BUY" oder "SELL"
    :return: Erwarteter Profit
    """
    try:
        # Typkonvertierung sicherstellen
        last_price = float(last_price)
        fee_percent = float(fee_percent)

        # Gebühren berechnen
        trade_fee = last_price * fee_percent
        logging.debug(f"Berechnung: last_price={last_price}, fee_percent={fee_percent}, trade_fee={trade_fee}")

        if signal == "BUY":
            # Kauf simuliert; kein Gewinn bis zum Verkauf
            profit = -trade_fee
        elif signal == "SELL":
            # Verkauf simuliert; einfacher Gewinn
            profit = last_price - trade_fee
        else:
            profit = 0

        logging.debug(f"Profit berechnet: {profit} für Signal: {signal}")
        return profit
    except Exception as e:
        logging.error(f"Fehler in calculate_profit: {e}", exc_info=True)
        raise

def update_ki_model(pair, rsi, signal, profit):
    """
    Aktualisiert das KI-Modell basierend auf den neuesten Trades.
    :param pair: Handelspaar
    :param rsi: RSI-Wert
    :param signal: Signal ("BUY", "SELL", "HOLD")
    :param profit: Erzielter Profit
    """
    logging.debug(f"Update KI-Modell: Pair={pair}, RSI={rsi}, Signal={signal}, Profit={profit}")
    # Beispielhafte Logik: KI-Training simulieren
    print(f"Trainiere KI-Modell mit: Pair={pair}, RSI={rsi}, Signal={signal}, Profit={profit}")
