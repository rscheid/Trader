from julia.api import Julia
Julia(compiled_modules=False)  # Initialisierung mit deaktivierten kompilierten Modulen

from julia import Main
from sklearn.ensemble import RandomForestRegressor
import numpy as np

# Julia-Skript laden
Main.include("math_models.jl")

# Monte-Carlo-Simulation in Julia aufrufen
def run_julia_monte_carlo(prices, steps, mu, sigma):
    """
    Ruft die Julia-Funktion für Monte-Carlo-Simulation auf.
    """
    return Main.monte_carlo(prices, steps, mu, sigma)

# KI-gestützte Optimierung der Monte-Carlo-Parameter
def optimize_monte_carlo(prices, trades):
    """
    Optimiert Monte-Carlo-Parameter (mu, sigma) basierend auf historischen Trades.
    """
    # Separate Modelle für mu und sigma
    X = np.array([[trade['mu'], trade['sigma']] for trade in trades])
    mu_targets = np.array([trade['mu'] for trade in trades])
    sigma_targets = np.array([trade['sigma'] for trade in trades])

    # Modell für mu
    mu_model = RandomForestRegressor()
    mu_model.fit(X, mu_targets)

    # Modell für sigma
    sigma_model = RandomForestRegressor()
    sigma_model.fit(X, sigma_targets)

    # Aktuelle Marktbedingungen
    current_mu = np.mean(np.diff(np.log(prices)))
    current_sigma = np.std(np.diff(np.log(prices)))

    # Optimierte Parameter vorhersagen
    optimized_mu = mu_model.predict([[current_mu, current_sigma]])[0]
    optimized_sigma = sigma_model.predict([[current_mu, current_sigma]])[0]

    return optimized_mu, optimized_sigma

# Logging-Funktion
def log_trade(action, price, mu, sigma, simulation_result, actual_price_after_trade=None):
    """
    Protokolliert die Trading-Entscheidungen in einer CSV-Datei.
    """
    with open("trade_log.csv", "a") as f:
        f.write(f"{action},{price},{mu},{sigma},{simulation_result},{actual_price_after_trade}\n")

# Haupt-Trading-Logik
def trading_with_julia(prices, past_trades):
    """
    Kombiniert Julia und KI für optimierte Trading-Entscheidungen.
    """
    # Optimierung der Parameter mit KI
    mu, sigma = optimize_monte_carlo(prices, past_trades)

    # Julia: Monte-Carlo-Simulation ausführen
    simulation = run_julia_monte_carlo(prices, steps=1000, mu=mu, sigma=sigma)

    # Entscheidungslogik
    if simulation[-1] > prices[-1] * 1.01:
        action = "BUY"
    elif simulation[-1] < prices[-1] * 0.99:
        action = "SELL"
    else:
        action = "HOLD"

    # Simulierter Preis nach der Entscheidung (z. B. in der Zukunft)
    actual_price_after_trade = prices[-1] * (1 + np.random.uniform(-0.02, 0.02))

    # Ergebnisse loggen
    log_trade(action, prices[-1], mu, sigma, simulation[-1], actual_price_after_trade)
    print(f"Trading-Entscheidung: {action} bei Preis {prices[-1]}, erwarteter Preis: {actual_price_after_trade}")
    return action

# Hauptprogramm
if __name__ == "__main__":
    # Beispiel: Preisdaten
    example_prices = [100 + np.sin(i / 10) * 5 for i in range(100)]

    # Beispiel: Historische Trades
    past_trades = [
        {'mu': 0.01, 'sigma': 0.2, 'profit': 50},
        {'mu': 0.02, 'sigma': 0.25, 'profit': -10},
        {'mu': 0.03, 'sigma': 0.3, 'profit': 70},
    ]

    # Mehrere Trades simulieren
    for _ in range(10):
        trading_with_julia(example_prices, past_trades)
