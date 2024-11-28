import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE

def train_model(log_file="trade_log.csv"):
    """
    Trainiert ein XGBoost-Modell mit optimierten Parametern und balancierten Daten.
    """
    # 1. Daten laden
    columns = ["Action", "Price", "Mu", "Sigma", "SimulationResult", "ActualPriceAfterTrade"]
    df = pd.read_csv(log_file, names=columns)

    # 2. Zielvariable (Success) erstellen
    df["Success"] = (df["ActualPriceAfterTrade"] > df["Price"]).astype(int)  # Für BUY
    df.loc[df["Action"] == "SELL", "Success"] = (df["ActualPriceAfterTrade"] < df["Price"]).astype(int)

    # Features und Ziel trennen
    X = df[["Price", "Mu", "Sigma", "SimulationResult"]]
    y = df["Success"]

    # 3. Klassenverteilung prüfen
    print("Klassenverteilung vor SMOTE:")
    print(y.value_counts())

    # 4. Daten balancieren mit SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    print("Klassenverteilung nach SMOTE:")
    print(pd.Series(y_resampled).value_counts())

    # 5. Stratified Train-Test-Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.3, stratify=y_resampled, random_state=42
    )

    # 6. XGBoost-Modell erstellen und trainieren
    model = xgb.XGBClassifier(
        use_label_encoder=False,
        eval_metric="logloss",
        n_estimators=200,  # Mehr Bäume
        max_depth=7,       # Größere Tiefe
        learning_rate=0.05 # Niedrigere Lernrate
    )
    model.fit(X_train, y_train)

    # 7. Vorhersagen und Ergebnisse auswerten
    y_pred = model.predict(X_test)

    print("\n--- Modellleistung ---")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # 8. Modell speichern
    model.save_model("xgboost_trading_model.json")
    print("\nDas Modell wurde als 'xgboost_trading_model.json' gespeichert.")
    return model

if __name__ == "__main__":
    train_model()
