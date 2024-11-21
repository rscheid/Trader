import logging
import sqlite3
from datetime import datetime
from trading_utility import fetch_candles, calculate_rsi, calculate_profit, update_ki_model

# Logging auf Expertenniveau
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logging.info("Starte Rudi-Bot auf Level 3...")

# Initialisiere die Datenbank
db_path = "trading_data.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Erstelle Tabelle, falls nicht vorhanden
cursor.execute("""
CREATE TABLE IF NOT EXISTS trades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pair TEXT,
    rsi REAL,
    signal TEXT,
    action TEXT,
    profit REAL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# Simulation von Handelspaaren
trading_pairs = ["BTC/USDT", "ETH/USDT", "XRP/USDT", "ADA/USDT"]

# Gebühren für Binance
FEE_PERCENT = 0.002

# Initialisiere KI-Modell (Platzhalter)
model = None  # TODO: Integriere ein LSTM-Modell

# Verarbeite Handelspaare
for pair in trading_pairs:
    logging.info(f"Verarbeite Handelspaar: {pair}")
    
    # Fetch historical data
    candles = fetch_candles(pair)
    if not candles:
        logging.warning(f"Keine Daten für {pair}. Überspringe.")
        continue

    # Schlusskurse extrahieren und RSI berechnen
    close_prices = [candle[4] for candle in candles]
    rsi = calculate_rsi(close_prices)
    logging.info(f"{pair} - RSI: {rsi:.2f}")

    # Signal basierend auf RSI
    if rsi < 30:
        signal = "BUY"
    elif rsi > 70:
        signal = "SELL"
    else:
        signal = "HOLD"

    # Trade-Logik mit Gebühren und Gewinnprüfung
    last_trade_price = close_prices[-1]
    trade_amount = 1  # Beispielhafte Menge
    expected_profit = calculate_profit(last_trade_price, FEE_PERCENT, signal)

    if signal in ["BUY", "SELL"] and expected_profit > 0:
        action = "Trade ausgeführt"
        logging.info(f"{pair} - Signal: {signal}, Aktion: {action}, Erwarteter Gewinn: {expected_profit:.8f}")
        
        # KI-Modell aktualisieren (falls implementiert)
        if model:
            update_ki_model(model, pair, rsi, signal, expected_profit)
    else:
        action = "Kein Trade"
        logging.info(f"{pair} - Signal: {signal}, Aktion: {action} (Unprofitabler Trade)")

    # Speichere Ergebnisse in DB
    cursor.execute("""
    INSERT INTO trades (pair, rsi, signal, action, profit)
    VALUES (?, ?, ?, ?, ?)
    """, (pair, rsi, signal, action, expected_profit))
    conn.commit()

logging.info("Verarbeitung abgeschlossen. Schließe Datenbank...")
conn.close()
