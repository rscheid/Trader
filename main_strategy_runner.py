import threading
import random
from ai_decision import decide_strategy
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from hft_strategy import hft_strategy
from swing_strategy import swing_strategy

def execute_hft():
    market_data = [100 + i * random.uniform(-0.2, 0.2) for i in range(100)]
    return hft_strategy(market_data)

def execute_swing():
    prices = [100 + i * random.uniform(-1, 1) for i in range(100)]
    return swing_strategy(prices)

if __name__ == "__main__":
    # KI-Training
    features = np.array([[0.01, 0.001], [0.05, 0.003], [0.2, 0.01]])
    labels = np.array([0, 0, 1])  # 0 = HFT, 1 = Swing Trading
    clf = DecisionTreeClassifier()
    clf.fit(features, labels)

    # Simulierter Marktstatus
    current_market = [0.15, 0.005]
    chosen_strategy = decide_strategy(current_market, clf)

    if chosen_strategy == "HFT":
        print("Starte HFT-Modell...")
        hft_thread = threading.Thread(target=execute_hft)
        hft_thread.start()
        hft_thread.join()
    else:
        print("Starte Swing-Trading-Modell...")
        swing_thread = threading.Thread(target=execute_swing)
        swing_thread.start()
        swing_thread.join()
