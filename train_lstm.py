import pandas as pd
import sqlite3
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import numpy as np
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_training_data():
    conn = sqlite3.connect("trading_data.db")
    query = "SELECT timestamp, rsi, last_price FROM trades WHERE rsi IS NOT NULL"
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Zeitstempel sortieren und auf Preis/RIS normalisieren
    df = df.sort_values("timestamp")
    return df

def preprocess_data(df):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(df[['rsi', 'last_price']])
    x_train, y_train = [], []
    lookback = 14  # Beispiel für den Zeitraum

    for i in range(lookback, len(scaled_data)):
        x_train.append(scaled_data[i - lookback:i, :])
        y_train.append(scaled_data[i, 0])  # Vorhersage basiert auf RSI

    return np.array(x_train), np.array(y_train), scaler

def build_lstm_model(input_shape):
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(units=50, return_sequences=False),
        Dropout(0.2),
        Dense(units=1)
    ])
    model.compile(optimizer="adam", loss="mean_squared_error")
    return model

def train_model():
    df = load_training_data()
    x_train, y_train, scaler = preprocess_data(df)
    
    model = build_lstm_model((x_train.shape[1], x_train.shape[2]))
    model.fit(x_train, y_train, epochs=10, batch_size=32)
    
    # Speichern des Modells
    model.save("lstm_model.h5")
    logging.info("LSTM-Modell erfolgreich trainiert und gespeichert.")

if __name__ == "__main__":
    train_model()
