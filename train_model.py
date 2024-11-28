import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

def train_model(log_file="trade_log.csv"):
    # Daten laden
    columns = ["Action", "Price", "Mu", "Sigma", "SimulationResult", "ActualPriceAfterTrade"]
    df = pd.read_csv(log_file, names=columns)

    # Zielvariable erstellen: 1 = Erfolg, 0 = Misserfolg
    df["Success"] = (df["ActualPriceAfterTrade"] > df["Price"]).astype(int)  # Für BUY
    df.loc[df["Action"] == "SELL", "Success"] = (df["ActualPriceAfterTrade"] < df["Price"]).astype(int)

    # Features und Ziel trennen
    X = df[["Price", "Mu", "Sigma", "SimulationResult"]]
    y = df["Success"]

    # Train/Test-Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # XGBoost-Modell trainieren
    model = xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss")
    model.fit(X_train, y_train)

    # Vorhersagen
    y_pred = model.predict(X_test)

    # Ergebnisse
    print("Trainings-Ergebnisse:")
    print(classification_report(y_test, y_pred))

    return model

if __name__ == "__main__":
    model = train_model()
