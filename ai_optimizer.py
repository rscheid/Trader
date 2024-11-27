from pysr import PySRRegressor
import numpy as np

def optimize_formula(data_x, data_y):
    model = PySRRegressor(
        niterations=100,  # Anzahl der Iterationen
        binary_operators=["+", "-", "*", "/"],
        unary_operators=["exp", "log", "sqrt", "square"],
        populations=1,
        verbosity=1,
    )
    model.fit(np.array(data_x).reshape(-1, 1), np.array(data_y))
    return model

# Beispiel-Daten
example_prices = [100, 101, 102, 103, 105, 104, 103, 102, 100, 98]
target_values = [x * 1.05 for x in example_prices]

print("Data X:", example_prices)
print("Data Y:", target_values)

print("Starte symbolische Regression...")
optimized_model = optimize_formula(example_prices, target_values)
print("Optimiertes Modell:", optimized_model)
