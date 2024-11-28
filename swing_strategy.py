import numpy as np
import random
import time  # Modul hinzufügen

def swing_strategy(prices, window=10, fee=0.002):
    """
    Swing-Trading-Strategie basierend auf Monte-Carlo und Bollinger-Bändern.
    """
    trades = []

    # Berechnung von Bollinger-Bändern
    ma = np.mean(prices[-window:])
    std_dev = np.std(prices[-window:])
    upper_band = ma + 2 * std_dev
    lower_band = ma - 2 * std_dev

    for i in range(5):  # Simuliere 5 Trades
        current_price = prices[-1] + random.uniform(-1, 1)
        if current_price < lower_band * (1 - fee):
            action = "BUY"
        elif current_price > upper_band * (1 + fee):
            action = "SELL"
        else:
            action = "HOLD"

        trades.append((action, current_price))
        print(f"Swing {action} at price: {current_price}")
        time.sleep(2)

    return trades

if __name__ == "__main__":
    swing_prices = [100 + i * random.uniform(-1, 1) for i in range(100)]
    swing_results = swing_strategy(swing_prices)
