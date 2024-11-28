import pandas as pd
import matplotlib.pyplot as plt

def analyze_trades(log_file="trade_log.csv"):
    """
    Analysiert die protokollierten Trades.
    """
    # CSV-Daten einlesen
    columns = ["Action", "Price", "Mu", "Sigma", "SimulationResult", "ActualPriceAfterTrade"]
    df = pd.read_csv(log_file, names=columns)

    # Übersicht der Daten
    print("\n--- Übersicht der Daten ---")
    print(df.head())

    # Statistiken zu den Aktionen
    print("\n--- Aktionen ---")
    print(df["Action"].value_counts())

    # Durchschnittswerte
    print("\n--- Durchschnittswerte ---")
    print(f"Durchschnittlicher Preis: {df['Price'].mean():.2f}")
    print(f"Durchschnittlicher ActualPriceAfterTrade: {df['ActualPriceAfterTrade'].mean():.2f}")
    print(f"Durchschnittliches Mu: {df['Mu'].mean():.4f}")
    print(f"Durchschnittliches Sigma: {df['Sigma'].mean():.4f}")

    # Performance-Bewertung
    print("\n--- Performance-Bewertung ---")
    sell_trades = df[df["Action"] == "SELL"]
    buy_trades = df[df["Action"] == "BUY"]

    # Erfolg von SELL: Ist der tatsächliche Preis niedriger?
    sell_success = sell_trades["ActualPriceAfterTrade"] < sell_trades["Price"]
    print(f"SELL-Erfolgsquote: {sell_success.mean() * 100:.2f}%")

    # Erfolg von BUY: Ist der tatsächliche Preis höher?
    buy_success = buy_trades["ActualPriceAfterTrade"] > buy_trades["Price"]
    print(f"BUY-Erfolgsquote: {buy_success.mean() * 100:.2f}%")

    # Plot erstellen: Preisverläufe
    plt.figure(figsize=(10, 6))
    plt.plot(df["Price"], label="Preis")
    plt.plot(df["ActualPriceAfterTrade"], label="Tatsächlicher Preis nach Trade")
    plt.legend()
    plt.title("Preisverlauf")
    plt.xlabel("Trades")
    plt.ylabel("Preis")
    plt.show()

    # Plot erstellen: Mu und Sigma
    plt.figure(figsize=(10, 6))
    plt.plot(df["Mu"], label="Mu (Drift)")
    plt.plot(df["Sigma"], label="Sigma (Volatilität)")
    plt.legend()
    plt.title("Optimierte Parameter (Mu und Sigma)")
    plt.xlabel("Trades")
    plt.ylabel("Wert")
    plt.show()

if __name__ == "__main__":
    analyze_trades()
