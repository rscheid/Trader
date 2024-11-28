import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from julia import Main  # PyJulia-Integration

# --- Julia-Skript einbinden ---
Main.include("math_models.jl")

# --- Python-Implementierungen ---
def moving_average(prices, window=5):
    """
    Berechnet den einfachen gleitenden Durchschnitt (SMA).
    """
    return pd.Series(prices).rolling(window=window).mean().tolist()

def volatility(prices, window=10):
    """
    Berechnet die Volatilität eines Assets.
    """
    log_returns = np.log(np.array(prices)[1:] / np.array(prices)[:-1])
    return pd.Series(log_returns).rolling(window=window).std().tolist()

def bollinger_bands(prices, window=10):
    """
    Berechnet Bollinger-Bänder.
    """
    ma = moving_average(prices, window)
    vol = volatility(prices, window)
    upper_band = [m + 2 * v if m is not None and v is not None else None for m, v in zip(ma, vol)]
    lower_band = [m - 2 * v if m is not None and v is not None else None for m, v in zip(ma, vol)]
    return ma, upper_band, lower_band

def plot_bollinger(prices, window=10):
    """
    Visualisiert Bollinger-Bänder.
    """
    ma, upper_band, lower_band = bollinger_bands(prices, window)
    plt.figure(figsize=(12, 6))
    plt.plot(prices, label="Preise")
    plt.plot(ma, label="Mittlere Linie (MA)", linestyle='--')
    plt.plot(upper_band, label="Oberes Band", linestyle=':')
    plt.plot(lower_band, label="Unteres Band", linestyle=':')
    plt.fill_between(range(len(prices)), lower_band, upper_band, color='gray', alpha=0.2)
    plt.title("Bollinger-Bänder")
    plt.xlabel("Zeit")
    plt.ylabel("Preis")
    plt.legend()
    plt.grid(True)
    plt.show()

# --- Julia-Integration für Monte-Carlo ---
def julia_monte_carlo(prices, steps=1000):
    """
    Nutzt Julia für die Monte-Carlo-Simulation.
    """
    mu = np.mean(np.diff(np.log(prices)))  # Durchschnittliche Rendite
    sigma = np.std(np.diff(np.log(prices)))  # Historische Volatilität
    simulation = Main.monte_carlo_simulation(prices, steps, mu, sigma)
    return simulation

def plot_monte_carlo_with_julia(prices, simulations=10, steps=1000):
    """
    Visualisiert mehrere Monte-Carlo-Simulationen mit Julia.
    """
    plt.figure(figsize=(12, 6))
    for _ in range(simulations):
        sim = julia_monte_carlo(prices, steps)
        plt.plot(sim, alpha=0.6)
    plt.title("Monte-Carlo-Simulationen (Julia)")
    plt.xlabel("Zeitschritte")
    plt.ylabel("Preis")
    plt.grid(True)
    plt.show()

# --- Trading-Logik ---
def trading_decision(prices):
    """
    Entscheidungslogik für den Trading-Bot basierend auf Analysen.
    """
    ma, upper_band, lower_band = bollinger_bands(prices)
    last_price = prices[-1]

    if last_price < lower_band[-1]:
        return "BUY", last_price
    elif last_price > upper_band[-1]:
        return "SELL", last_price
    else:
        return "HOLD", last_price

# --- Hauptprogramm ---
if __name__ == "__main__":
    # Beispiel-Daten (synthetische Preise)
    example_prices = [100 + np.sin(i / 10) * 5 for i in range(100)]

    # Visualisierung der Bollinger-Bänder
    plot_bollinger(example_prices)

    # Monte-Carlo-Simulationen mit Julia
    plot_monte_carlo_with_julia(example_prices)

    # Trading-Entscheidung
    decision, price = trading_decision(example_prices)
    print(f"Entscheidung: {decision} bei Preis: {price}")
