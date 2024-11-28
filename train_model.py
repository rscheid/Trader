import warnings
warnings.filterwarnings(action="ignore", category=UserWarning, module="xgboost")

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE

def calculate_rsi(prices, window=14):
    """
    Berechnet den Relative Strength Index (RSI).
    """
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def train_model(log_file="trade_log.csv"):
    """
    Trainiert ein XGBoost-Modell mit vollständiger Grid-Search, Zwischenspeicherung und Parallelisierung.
    """
    # 1. Daten laden
    columns = ["Action", "Price", "Mu", "Sigma", "SimulationResult", "ActualPriceAfterTrade"]
    df = pd.read_csv(log_file, names=columns)

    # 2. Zielvariable (Success) erstellen
    df["Success"] = (df["ActualPriceAfterTrade"] > df["Price"]).astype(int)  # Für BUY
    df.loc[df["Action"] == "SELL", "Success"] = (df["ActualPriceAfterTrade"] < df["Price"]).astype(int)

    # 3. Zusätzliche Features hinzufügen
    df["PriceChange"] = (df["Price"] - df["Price"].shift(1)) / df["Price"].shift(1)
    df["MovingAverage"] = df["Price"].rolling(window=5).mean()
    df["Volatility"] = df["Price"].rolling(window=5).std()
    df["RSI"] = calculate_rsi(df["Price"])
    df["Momentum"] = df["Price"] - df["Price"].shift(5)
    df = df.fillna(0)  # Fehlende Werte auffüllen

    # Features und Ziel trennen
    X = df[["Price", "Mu", "Sigma", "SimulationResult", "PriceChange", "MovingAverage", "Volatility", "RSI", "Momentum"]]
    y = df["Success"]

    # 4. Klassenverteilung prüfen
    print("Klassenverteilung vor SMOTE:")
    print(y.value_counts())

    # 5. Daten balancieren mit SMOTE
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    print("Klassenverteilung nach SMOTE:")
    print(pd.Series(y_resampled).value_counts())

    # 6. Stratified Train-Test-Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.3, stratify=y_resampled, random_state=42
    )

    # 7. Grid-Search für Hyperparameter-Optimierung
    param_grid = {
        "n_estimators": [100, 300, 500],
        "max_depth": [5, 10, 15],
        "learning_rate": [0.01, 0.03, 0.1],
        "subsample": [0.8],
        "colsample_bytree": [0.8]
    }

    grid_search = GridSearchCV(
        estimator=xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss"),
        param_grid=param_grid,
        scoring="accuracy",
        cv=5,
        verbose=1,
        n_jobs=-1  # Nutze alle verfügbaren CPU-Kerne
    )

    # Grid-Search mit Zwischenspeicherung der Ergebnisse
    try:
        grid_search.fit(X_train, y_train)
        results = pd.DataFrame(grid_search.cv_results_)
        results.to_csv("grid_search_results.csv", index=False)
        print(f"\nBeste Parameter: {grid_search.best_params_}")
    except KeyboardInterrupt:
        print("\nGrid-Search wurde abgebrochen. Zwischenergebnisse werden gespeichert.")
        results = pd.DataFrame(grid_search.cv_results_)
        results.to_csv("grid_search_results_partial.csv", index=False)
        return

    # 8. Bestes Modell trainieren
    best_model = grid_search.best_estimator_
    best_model.fit(X_train, y_train)

    # 9. Cross-Validation Accuracy
    scores = cross_val_score(best_model, X_resampled, y_resampled, cv=5, scoring="accuracy")
    print(f"\nCross-Validation Accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})")

    # 10. Vorhersagen und Ergebnisse auswerten
    y_pred = best_model.predict(X_test)

    print("\n--- Modellleistung ---")
    print(f"Accuracy (Testdaten): {accuracy_score(y_test, y_pred):.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    # 11. Modell speichern
    best_model.save_model("xgboost_trading_model.json")
    print("\nDas Modell wurde als 'xgboost_trading_model.json' gespeichert.")
    return best_model

if __name__ == "__main__":
    train_model()
