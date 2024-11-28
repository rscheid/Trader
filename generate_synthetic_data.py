import numpy as np
import pandas as pd

def generate_synthetic_data(file_name="trade_log.csv", n=1000):
    """
    Generiert synthetische Trade-Daten für das Modelltraining.
    """
    np.random.seed(42)  # Reproduzierbarkeit
    data = {
        "Action": np.random.choice(["BUY", "SELL"], size=n),
        "Price": np.random.uniform(90, 110, size=n),
        "Mu": np.random.uniform(0.01, 0.05, size=n),
        "Sigma": np.random.uniform(0.1, 0.5, size=n),
        "SimulationResult": np.random.uniform(90, 110, size=n),
        "ActualPriceAfterTrade": np.random.uniform(90, 110, size=n),
    }
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False, header=False)
    print(f"Synthetische Daten wurden in {file_name} gespeichert.")

if __name__ == "__main__":
    generate_synthetic_data()
