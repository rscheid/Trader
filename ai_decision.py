from sklearn.tree import DecisionTreeClassifier
import numpy as np

def decide_strategy(market_features, model):
    """
    Entscheidet, welche Strategie verwendet wird.
    """
    decision = model.predict([market_features])
    return "HFT" if decision[0] == 0 else "Swing Trading"

if __name__ == "__main__":
    # Trainingsdaten
    features = np.array([[0.01, 0.001], [0.05, 0.003], [0.2, 0.01]])
    labels = np.array([0, 0, 1])  # 0 = HFT, 1 = Swing Trading

    # Modell trainieren
    clf = DecisionTreeClassifier()
    clf.fit(features, labels)

    # Simulierter Marktstatus
    current_market = [0.15, 0.005]
    chosen_strategy = decide_strategy(current_market, clf)
    print(f"KI entscheidet: {chosen_strategy}")
