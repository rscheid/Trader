import numpy as np

def calculate_rsi(closes, period=14):
    """
    Berechnet den Relative Strength Index (RSI).
    :param closes: Liste der Schlusskurse
    :param period: Berechnungszeitraum (Standard: 14)
    :return: RSI-Wert
    """
    if len(closes) < period:
        raise ValueError("Nicht genügend Schlusskurse für die RSI-Berechnung.")

    closes = np.array(closes)
    deltas = np.diff(closes)
    gains = np.where(deltas > 0, deltas, 0)
    losses = np.where(deltas < 0, -deltas, 0)

    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])

    if avg_loss == 0:
        return 100  # Maximaler RSI-Wert, wenn keine Verluste

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi
