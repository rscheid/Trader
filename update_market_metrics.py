import sqlite3
from binance.client import Client
import os
import time
from requests.exceptions import RequestException

# Binance API-Schlüssel
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_SECRET_KEY")


def sanitize_symbol(symbol):
    """
    Bereinigt Symbole für die Binance-API.
    """
    sanitized = symbol.split(":")[0].split("-")[0].replace("/", "").upper()
    if len(sanitized) > 20 or not sanitized.isalnum():
        print(f"Ungültiges Symbol übersprungen: {symbol}")
        return None
    return sanitized


def fetch_kline_data(symbol, retries=3):
    """
    Ruft Kline-Daten von der Binance-API ab, mit Wiederholungslogik bei Fehlern.
    """
    for attempt in range(retries):
        try:
            client = Client(API_KEY, API_SECRET)
            klines = client.get_klines(symbol=symbol, interval="1h", limit=24)
            return klines
        except Exception as e:
            print(f"Fehler bei API-Anfrage {symbol}: {e}. Versuch {attempt + 1}")
            time.sleep(1)
    print(f"Fehlgeschlagen bei {symbol} nach {retries} Versuchen.")
    return None


def update_market_metrics(db_path="trading_data.db"):
    """
    Aktualisiert die Spalten `volume_24h` und `volatility_24h` in der Datenbank.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT symbol FROM binance_markets WHERE is_active = 1 AND market_type = 'spot';
    """)
    markets = cursor.fetchall()

    if not markets:
        print("Keine Symbole zur Verarbeitung gefunden.")
        conn.close()
        return

    # Protokolldateien erstellen/leeren
    with open("skipped_symbols.txt", "w") as skipped_log:
        skipped_log.write("")

    with open("error_log.txt", "w") as error_log:
        error_log.write("")

    for market in markets:
        original_symbol = market[0]
        sanitized_symbol = sanitize_symbol(original_symbol)
        if not sanitized_symbol:
            with open("skipped_symbols.txt", "a") as log:
                log.write(f"{original_symbol}\n")
            continue

        data = fetch_kline_data(sanitized_symbol)
        if data is None:
            print(f"Daten für {original_symbol} konnten nicht abgerufen werden.")
            with open("error_log.txt", "a") as log:
                log.write(f"{original_symbol} - Keine Daten abgerufen\n")
            continue

        try:
            # Daten verarbeiten
            volume_24h = sum([float(k[5]) for k in data])
            volatility_24h = (max([float(k[2]) for k in data]) - min([float(k[3]) for k in data])) / min([float(k[3]) for k in data])

            # Werte in der Datenbank aktualisieren
            cursor.execute("""
            UPDATE binance_markets
            SET volume_24h = ?, volatility_24h = ?
            WHERE symbol = ?;
            """, (volume_24h, volatility_24h, original_symbol))
            print(f"Symbol {original_symbol} erfolgreich aktualisiert: Volumen={volume_24h:.2f}, Volatilität={volatility_24h:.4f}")

        except Exception as e:
            print(f"Fehler beim Aktualisieren von {original_symbol}: {e}")
            with open("error_log.txt", "a") as log:
                log.write(f"{original_symbol} - {e}\n")

    conn.commit()
    conn.close()
    print("Aktualisierung abgeschlossen. Siehe 'error_log.txt' und 'skipped_symbols.txt' für Details.")


if __name__ == "__main__":
    if not API_KEY or not API_SECRET:
        print("Fehler: API-Schlüssel nicht gesetzt!")
    else:
        update_market_metrics()
