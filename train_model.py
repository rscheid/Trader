import warnings
warnings.filterwarnings(action="ignore", category=UserWarning, module="xgboost")

import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from imblearn.over_sampling import SMOTE

# Funktionen zur Berechnung der Features
def calculate_ask_bid_spread(ask_prices, bid_prices):
    return (ask_prices - bid_prices) / ((ask_prices + bid_prices) / 2)

def calculate_relative_price_change(prices, window=5):
    return prices.pct_change(periods=window)

def calculate_volume_ratio(buy_volume, sell_volume):
    return buy_volume / (sell_volume + 1e-8)

def calculate_volatility_cluster(prices, window=10):
    return prices.rolling(window=window).std()

def calculate_rsi(prices, window=14):
    delta = prices.diff()
    gain = delta.where(delta > 0, 0).rolling(window=window).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def add_features(df):
    """
    Fügt erweiterte Features zum DataFrame hinzu.
    """
    if "AskPrice" in df.columns and "BidPrice" in df.columns:
        df["AskBidSpread"] = calculate_ask_bid_spread(df["AskPrice"], df["BidPrice"])
    else:
        df["AskBidSpread"] = 0  # Platzhalter

    df["RelativePriceChange"] = calculate_relative_price_change(df["Price"], window=5)

    if "BuyVolume" in df.columns and "SellVolume" in df.columns:
        df["VolumeRatio"] = calculate_volume_ratio(df["BuyVolume"], df["SellVolume"])
    else:
        df["VolumeRatio"] = 0  # Platzhalter

    df["RSI_Short"] = calculate_rsi(df["Price"], window=14)
    df["RSI_Long"] = calculate_rsi(df["Price"], window=50)

    df["VolatilityCluster"] = calculate_volatility_cluster(df["Price"], window=10)

    df = df.fillna(0)
    return df

# Hauptfunktion für das Training
def train_model(log_file="trade_log.csv"):
    """
    Trainiert ein XGBoost-Modell mit erweiterten Features.
    """
    # 1. Daten laden
    columns = ["Action", "Price", "Mu", "Sigma", "SimulationResult", "ActualPriceAfterTrade"]
    df = pd.read_csv(log_file, names=columns)

    # Dummy-Werte für fehlende Spalten
    if "AskPrice" not in df.columns:
        df["AskPrice"] = df["Price"] * 1.01  # Dummy: 1% höher als Preis
    if "BidPrice" not in df.columns:
        df["BidPrice"] = df["Price"] * 0.99  # Dummy: 1% niedriger als Preis
    if "BuyVolume" not in df.columns:
        df["BuyVolume"] = np.random.uniform(50, 100, size=len(df))
    if "SellVolume" not in df.columns:
        df["SellVolume"] = np.random.uniform(40, 90, size=len(df))

    # Features hinzufügen
    df = add_features(df)

    # Zielvariable (Success) erstellen
    df["Success"] = (df["ActualPriceAfterTrade"] > df["Price"]).astype(int)
    df.loc[df["Action"] == "SELL", "Success"] = (df["ActualPriceAfterTrade"] < df["Price"]).astype(int)

    # Features und Ziel trennen
    feature_columns = [
        "Price", "Mu", "Sigma", "SimulationResult", "AskBidSpread", 
        "RelativePriceChange", "VolumeRatio", "RSI_Short", "RSI_Long", "VolatilityCluster"
    ]
    X = df[feature_columns]
    y = df["Success"]

    # SMOTE für Balancierung
    smote = SMOTE(random_state=42)
    X_resampled, y_resampled = smote.fit_resample(X, y)

    # Train-Test-Split
    X_train, X_test, y_train, y_test = train_test_split(
        X_resampled, y_resampled, test_size=0.3, stratify=y_resampled, random_state=42
    )

    # Grid-Search für Hyperparameter
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
        n_jobs=-1
    )

    grid_search.fit(X_train, y_train)
    print(f"\nBeste Parameter: {grid_search.best_params_}")

    best_model = grid_search.best_estimator_
    best_model.fit(X_train, y_train)

    scores = cross_val_score(best_model, X_resampled, y_resampled, cv=5, scoring="accuracy")
    print(f"\nCross-Validation Accuracy: {scores.mean():.2f} (+/- {scores.std():.2f})")

    y_pred = best_model.predict(X_test)
    print("\n--- Modellleistung ---")
    print(f"Accuracy (Testdaten): {accuracy_score(y_test, y_pred):.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))

    best_model.save_model("xgboost_trading_model.json")
    print("\nDas Modell wurde als 'xgboost_trading_model.json' gespeichert.")

if __name__ == "__main__":
    train_model()
