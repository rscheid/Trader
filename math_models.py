import numpy as np
import pandas as pd

def monte_carlo_simulation(prices, steps=1000, mu=0.05, sigma=0.2):
    """
    Simuliert die Preisbewegung eines Assets mit Monte-Carlo-Simulation.

    :param prices: Liste der bisherigen Preise.
    :param steps: Anzahl der Schritte in der Simulation.
    :param mu: Erwartete Rendite (Drift).
    :param sigma: Volatilität (Volatility).
    :return: Simulierte Preisentwicklung als Liste.
    """
    dt = 1 / steps
    last_price = prices[-1]  # Startwert ist der letzte bekannte Preis
    simulation = [last_price]

    for _ in range(steps):
        drift = (mu - 0.5 * sigma**2) * dt
        shock = sigma * np.sqrt(dt) * np.random.normal()
        next_price = simulation[-1] * np.exp(drift + shock)
        simulation.append(next_price)

    return simulation

def fourier_analysis(prices):
    """
    Führt eine Fourier-Analyse auf den Preisdaten durch, um dominante Frequenzen zu extrahieren.

    :param prices: Liste oder NumPy-Array der Preise.
    :return: Frequenzkomponenten und deren Amplituden.
    """
    prices_array = np.array(prices)
    fft_result = np.fft.fft(prices_array)
    frequencies = np.fft.fftfreq(len(prices_array))

    # Nur positive Frequenzen und zugehörige Amplituden
    positive_freqs = frequencies[frequencies >= 0]
    amplitudes = np.abs(fft_result[frequencies >= 0])

    return positive_freqs, amplitudes

def moving_average(prices, window=5):
    """
    Berechnet den gleitenden Durchschnitt (Moving Average).

    :param prices: Liste der Preise.
    :param window: Fenstergröße für den gleitenden Durchschnitt.
    :return: Liste der gleitenden Durchschnitte.
    """
    return pd.Series(prices).rolling(window=window).mean().tolist()

def volatility(prices, window=10):
    """
    Berechnet die Volatilität eines Assets über ein gegebenes Fenster.

    :param prices: Liste der Preise.
    :param window: Fenstergröße für die Berechnung.
    :return: Liste der Volatilitätswerte.
    """
    log_returns = np.log(np.array(prices)[1:] / np.array(prices)[:-1])
    return pd.Series(log_returns).rolling(window=window).std().tolist()

if __name__ == "__main__":
    # Beispiel-Daten (künstliche Preisdaten)
    example_prices = [100, 101, 102, 103, 105, 104, 103, 102, 100, 98]

    print("Monte-Carlo-Simulation:")
    mc_simulation = monte_carlo_simulation(example_prices)
    print(mc_simulation[:10])  # Ausgabe der ersten 10 simulierten Preise

    print("\nFourier-Analyse:")
    freqs, amps = fourier_analysis(example_prices)
    print("Frequenzen:", freqs)
    print("Amplituden:", amps)

    print("\nGleitender Durchschnitt (5er Fenster):")
    ma = moving_average(example_prices, window=5)
    print(ma)

    print("\nVolatilität (10er Fenster):")
    vol = volatility(example_prices, window=10)
    print(vol)
