#!/bin/bash

# Variablen
CONTAINER_NAME="trading_bot_container"
DB_PATH="/app/trading_data.db"
LOG_FILE="bot_monitor.log"
API_LOG_FILE="api_monitor.log"

# Funktion: Nachricht mit Zeitstempel loggen
log_message() {
    local MESSAGE=$1
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $MESSAGE" | tee -a $LOG_FILE
}

# Funktion: Docker-Container prüfen
check_container() {
    log_message "Prüfe Docker-Container..."
    docker ps | grep $CONTAINER_NAME > /dev/null
    if [ $? -eq 0 ]; then
        log_message "Docker-Container läuft: $CONTAINER_NAME"
    else
        log_message "FEHLER: Docker-Container $CONTAINER_NAME läuft nicht."
    fi
}

# Funktion: Datenbank prüfen
check_database() {
    log_message "Prüfe Datenbank: $DB_PATH..."
    docker exec -it $CONTAINER_NAME sqlite3 $DB_PATH "SELECT count(*) FROM trades;" 2>/dev/null | tee -a $LOG_FILE
    if [ $? -eq 0 ]; then
        log_message "Datenbank ist verfügbar und enthält Einträge."
    else
        log_message "FEHLER: Datenbank $DB_PATH nicht verfügbar oder leer."
    fi
}

# Funktion: Logs auf Fehler prüfen
check_logs() {
    log_message "Prüfe Docker-Logs..."
    docker logs $CONTAINER_NAME 2>&1 | grep -i "error" | tee -a $LOG_FILE
    if [ $? -eq 0 ]; then
        log_message "FEHLER: Fehler in den Logs gefunden."
    else
        log_message "Keine Fehler in den Logs gefunden."
    fi
}

# Funktion: Handelsaktivität prüfen
check_trading_activity() {
    log_message "Prüfe Handelsaktivität (Testnet)..."
    docker exec -it $CONTAINER_NAME python3 -c "
from binance.client import Client
client = Client(api_key='DEINE_API_KEY', api_secret='DEIN_API_SECRET', testnet=True)
orders = client.get_open_orders()
balances = client.get_account()['balances']
print('Offene Orders:', orders)
print('Kontostände:', balances)
" 2>&1 | tee -a $API_LOG_FILE
}

# Funktion: KI-Status prüfen
check_ki_status() {
    log_message "Prüfe KI-Status..."
    docker exec -it $CONTAINER_NAME ps aux | grep process_all_pairs.py | grep -v grep > /dev/null
    if [ $? -eq 0 ]; then
        log_message "KI-Skript läuft: process_all_pairs.py"
    else
        log_message "FEHLER: KI-Skript process_all_pairs.py läuft nicht."
    fi
}

# Hauptablauf
log_message "Starte Überprüfung von Bot, KI und Datenbanken."
check_container
check_database
check_logs
check_ki_status
check_trading_activity
log_message "Überprüfung abgeschlossen."

# Optional: Alle 30 Minuten wiederholen
read -p "Skript alle 30 Minuten ausführen? (y/n): " REPEAT
if [ "$REPEAT" == "y" ]; then
    while true; do
        sleep 1800
        log_message "Starte erneute Überprüfung..."
        check_container
        check_database
        check_logs
        check_ki_status
        check_trading_activity
    done
else
    log_message "Skript beendet. Keine Wiederholung eingestellt."
fi
