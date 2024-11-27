import sqlite3
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import logging

# Konfiguration des Logs
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DB_PATH = "trading_data.db"
MODEL_PATH = "lstm_model.h5"

def load_training_data():
    """
    Lädt die Trainingsdaten aus der Datenbank und gibt sie als DataFrame zurück.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        query = "SELECT timestamp, rsi, profit FROM training_data WHERE rsi IS NOT NULL AND profit IS NOT NULL"
        data = pd.read_sql_query(query, conn)
        conn.close()
        logging.info(f"{len(data)} Datensätze erfolgreich geladen.")
        return data
    except Exception as e:
        logging.error(f"Fehler beim Laden der Trainingsdaten: {e}")
        return pd.DataFrame()

def preprocess_data(data):
    """
    Bereitet die Daten für das LSTM-Modell vor.
    """
    try:
        # Sortiere die Daten nach Zeit
        data = data.sort_values(by="timestamp")
        
        # Normalisiere die RSI-Werte und Profite
        scaler = MinMaxScaler(feature_range=(0, 1))
        scaled_data = scaler.fit_transform(data[["rsi", "profit"]])

        # Erstelle Sequenzen für LSTM
        sequence_length = 14
        X, y = [], []
        for i in range(len(scaled_data) - sequence_length):
            X.append(scaled_data[i:i + sequence_length, 0])  # RSI-Werte
            y.append(scaled_data[i + sequence_length, 1])   # Profite

        X = np.array(X)
        y = np.array(y)
        X = np.expand_dims(X, axis=-1)  # LSTM erwartet 3D-Daten
        logging.info("Daten erfolgreich vorbereitet.")
        return X, y, scaler
    except Exception as e:
        logging.error(f"Fehler bei der Datenvorbereitung: {e}")
        return None, None, None

def train_model(X, y):
    """
    Trainiert das LSTM-Modell und gibt es zurück.
    """
    try:
        model = Sequential([
            LSTM(50, return_sequences=True, input_shape=(X.shape[1], X.shape[2])),
            LSTM(50, return_sequences=False),
            Dense(1)  # Ausgabe: Profit-Vorhersage
        ])
        model.compile(optimizer="adam", loss="mean_squared_error")
        model.fit(X, y, epochs=20, batch_size=32, verbose=1)
        logging.info("Modell erfolgreich trainiert.")
        return model
    except Exception as e:
        logging.error(f"Fehler beim Training des Modells: {e}")
        return None

if __name__ == "__main__":
    logging.info("LSTM-Modelltraining gestartet...")
    
    # Daten laden und vorbereiten
    data = load_training_data()
    if data.empty:
        logging.error("Keine Daten zum Trainieren gefunden.")
        exit()

    X, y, scaler = preprocess_data(data)
    if X is None or y is None:
        logging.error("Fehler bei der Datenvorbereitung.")
        exit()

    # Modell trainieren
    model = train_model(X, y)
    if model:
        # Modell speichern
        model.save(MODEL_PATH)
        logging.info(f"Modell gespeichert unter {MODEL_PATH}.")
    else:
        logging.error("Modelltraining fehlgeschlagen.")
