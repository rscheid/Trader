import time
import random

def hft_strategy(market_data, fee=0.002):
    """
    High-Frequency-Trading-Strategie.
    """
    trades = []
    for i in range(10):  # Simuliere 10 schnelle Trades
        price = market_data[-1] + random.uniform(-0.5, 0.5)
        action = "BUY" if random.random() > 0.5 else "SELL"

        # Gebühren berücksichtigen
        if action == "BUY":
            adjusted_price = price * (1 + fee)
        else:
            adjusted_price = price * (1 - fee)

        trades.append((action, adjusted_price))
        print(f"HFT {action} at price: {adjusted_price}")
        time.sleep(0.5)

    return trades

if __name__ == "__main__":
    market_data = [100 + i * random.uniform(-0.2, 0.2) for i in range(100)]
    hft_results = hft_strategy(market_data)
