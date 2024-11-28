from pysr import PySRRegressor
import numpy as np
import pandas as pd

# Daten generieren (Beispiel für Trainingsdaten)
def generate_training_data():
    """
    Simuliert Trainingsdaten für die Formeloptimierung.
    """
    prices = np.linspace(90, 110, 100)  # Beispielpreise
    mu = 0.01  # Drift
    sigma = 0.2  # Volatilität
    simulation_results = prices * (1 + mu - 0.5 * sigma ** 2)  # Simulierte Ergebnisse
    success = (simulation_results > prices).astype(int)  # 1, wenn Trade erfolgreich war
    return pd.DataFrame({"Price": prices, "Mu": mu, "Sigma": sigma, "Result": simulation_results, "Success": success})

# PySR-Modell erstellen
def optimize_formula(data):
    """
    Optimiert die mathematische Formel basierend auf den Trainingsdaten.
    """
    X = data[["Price", "Mu", "Sigma"]]
    y = data["Result"]

    # Symbolische Regression
    model = PySRRegressor(
        model_selection="best",
        niterations=50,  # Anzahl der Iterationen erhöhen bei mehr Daten
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["exp", "log", "sqrt"],
    )
    model.fit(X, y)
    return model

if __name__ == "__main__":
    # Trainingsdaten generieren
    data = generate_training_data()

    # Formeloptimierung starten
    model = optimize_formula(data)
    print("Optimierte Formel:")
    print(model)
