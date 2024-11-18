import ccxt
import logging
from dotenv import load_dotenv
import os

# .env-Datei laden
load_dotenv()

# Binance Testnet-API-Schlüssel aus Umgebungsvariablen lesen
API_KEY = os.getenv("TESTNET_API_KEY")
SECRET_KEY = os.getenv("TESTNET_SECRET")

# Verbindung zur Binance Testnet API herstellen
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': SECRET_KEY,
    'enableRateLimit': True,
})

# Testnet aktivieren
exchange.set_sandbox_mode(True)

# Logger konfigurieren
logging.basicConfig(
    filename="/app/trading_bot.log",  # Absoluter Pfad im Container
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def calculate_rsi(closes):
    """Berechnet den RSI basierend auf Schlusskursen."""
    gains = [closes[i] - closes[i - 1] for i in range(1, len(closes)) if closes[i] > closes[i - 1]]
    losses = [closes[i - 1] - closes[i] for i in range(1, len(closes)) if closes[i] < closes[i - 1]]

    avg_gain = sum(gains) / len(gains) if gains else 0
    avg_loss = sum(losses) / len(losses) if losses else 1  # Kein Verlust = künstlich 1

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def get_rsi_signal(symbol="BTC/USDT", timeframe="1m", limit=14):
    """Holt Marktdaten, berechnet den RSI und gibt ein Signal zurück."""
    try:
        candles = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
        closes = [c[4] for c in candles]

        rsi = calculate_rsi(closes)

        if rsi < 30:
            return "BUY", rsi
        elif rsi > 30:
            return "SELL", rsi
        else:
            return "HOLD", rsi
    except Exception as e:
        logging.error(f"Error in get_rsi_signal: {e}")
        return "ERROR", None

def execute_trade(signal, symbol="BTC/USDT", amount=0.001):
    """Führt basierend auf dem Signal einen simulierten Trade aus."""
    try:
        # Vor dem Ausführen eines Trades loggen
        logging.info(f"Attempting to execute {signal} order for {amount} {symbol}")
        
        # BUY-Order
        if signal == "BUY":
            order = exchange.create_market_buy_order(symbol, amount)
            logging.info(f"Executed BUY order: {order}")
            return f"BUY order executed: {order}"
        
        # SELL-Order
        elif signal == "SELL":
            order = exchange.create_market_sell_order(symbol, amount)
            logging.info(f"Executed SELL order: {order}")
            return f"SELL order executed: {order}"
        
        # HOLD-Signal
        else:
            logging.info("No trade executed (HOLD)")
            return "No trade executed (HOLD)"
    
    # Fehler abfangen und ins Log schreiben
    except Exception as e:
        logging.error(f"Error in execute_trade: {e}")
        return f"Error executing trade: {e}"

if __name__ == "__main__":
    # Beispielaufruf
    symbol = "BTC/USDT"
    amount = 0.001

    signal, rsi = get_rsi_signal(symbol)
    if signal != "ERROR":
        print(f"{signal} Signal: RSI={rsi:.2f}")
        trade_result = execute_trade(signal, symbol, amount)
        print(trade_result)
    else:
        print("Error calculating RSI")
