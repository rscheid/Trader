import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

# Daten laden (z. B. historische OHLCV-Daten von Binance)
def load_data(file_path, seq_len):
    data = pd.read_csv(file_path)
    data['RSI'] = calculate_rsi(data['Close'])
    
    # Normalisierung
    data_scaled = (data - data.min()) / (data.max() - data.min())
    
    # Sequenzen erstellen
    x, y = [], []
    for i in range(seq_len, len(data_scaled)):
        x.append(data_scaled.iloc[i-seq_len:i].values)
        y.append(data_scaled.iloc[i]['Close'])
    return np.array(x), np.array(y)

# RSI berechnen
def calculate_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# LSTM-Modell erstellen
def create_lstm_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dropout(0.2))
    model.add(Dense(1))  # Vorhersage für den Preis
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# Hauptfunktion
if __name__ == "__main__":
    # Pfad zur CSV-Datei mit historischen Daten
    file_path = "historical_data.csv"  # Ersetze durch echten Pfad
    seq_len = 60  # Länge der Sequenz (z. B. 60 Minuten)
    
    # Daten laden
    x, y = load_data(file_path, seq_len)
    train_size = int(len(x) * 0.8)
    x_train, y_train = x[:train_size], y[:train_size]
    x_test, y_test = x[train_size:], y[train_size:]

    # LSTM-Modell erstellen
    model = create_lstm_model((x_train.shape[1], x_train.shape[2]))
    
    # Modell trainieren
    history = model.fit(x_train, y_train, epochs=10, batch_size=32, validation_data=(x_test, y_test))
    
    # Ergebnisse plotten
    plt.plot(history.history['loss'], label='Training Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.legend()
    plt.show()

    # Modell speichern
    model.save("lstm_trading_model.h5")
