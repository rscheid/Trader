from julia.api import Julia
Julia(compiled_modules=False)

from julia import Main

# Julia-Skript laden
Main.include("math_models.jl")

# Beispielpreise
example_prices = [100.0, 101.0, 102.0, 103.0, 104.0]

# Monte-Carlo-Simulation aus Julia
def julia_monte_carlo(prices, steps=1000):
    mu = 0.05
    sigma = 0.2
    return Main.monte_carlo_simulation(prices, steps, mu, sigma)

# Simulation ausführen und Ergebnisse anzeigen
julia_simulation = julia_monte_carlo(example_prices)
print("Julia Monte-Carlo Simulation (erste 10 Preise):", julia_simulation[:10])
