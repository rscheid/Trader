#!/bin/bash

# Variablen
IMAGE_NAME="trading_bot_image"
CONTAINER_NAME="trading_bot_container"
PORT_MAPPING="3000:3000"
LOG_FILE="/app/logs/startdocker.log"
DOCKER_DATA_PATH="/mnt/blockstorage/docker"
APP_PATH="/dev/vda2/trading-bot"

# Sicherstellen, dass das Log-Verzeichnis existiert
mkdir -p $(dirname "$LOG_FILE")

# Funktion: Nachricht mit Zeitstempel loggen
log_message() {
    local MESSAGE=$1
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $MESSAGE" | tee -a $LOG_FILE
}

# Funktion: Speicherort prüfen
verify_docker_storage() {
    log_message "Überprüfe Docker-Datenpfad..."
    CURRENT_STORAGE=$(docker info | grep "Docker Root Dir" | awk '{print $4}')
    if [[ "$CURRENT_STORAGE" != "$DOCKER_DATA_PATH" ]]; then
        log_message "FEHLER: Docker verwendet nicht den vorgesehenen Speicherort ($DOCKER_DATA_PATH). Skript abgebrochen."
        exit 1
    else
        log_message "Docker-Datenpfad korrekt eingestellt ($DOCKER_DATA_PATH)."
    fi
}

# Docker-Host bereinigen
cleanup_docker() {
    read -p "Möchtest du Docker bereinigen? (y/n): " CLEANUP_OPTION
    if [ "$CLEANUP_OPTION" == "y" ]; then
        log_message "Docker bereinigen..."
        docker system prune -a --volumes -f
    else
        log_message "Docker-Bereinigung übersprungen."
    fi
}

# Temporäre Dateien bereinigen
cleanup_temp_files() {
    log_message "Temporäre Dateien bereinigen..."
    find $APP_PATH -name "__pycache__" -type d -exec rm -rf {} +
    rm -rf $APP_PATH/*.log /tmp/*
}

# Docker-Image bauen
build_container() {
    log_message "Baue Docker-Image..."
    docker build -t $IMAGE_NAME $APP_PATH >> $LOG_FILE 2>&1
    if [ $? -ne 0 ]; then
        log_message "Fehler beim Bauen des Docker-Images."
        exit 1
    fi
}

# Vorherigen Container stoppen und entfernen
stop_and_remove_container() {
    log_message "Stoppe und entferne bestehenden Container..."
    docker stop $CONTAINER_NAME 2>/dev/null
    docker rm $CONTAINER_NAME 2>/dev/null
}

# Docker-Container starten
start_container() {
    log_message "Starte Docker-Container..."
    docker run -dit --name $CONTAINER_NAME \
        -p $PORT_MAPPING \
        -v $DOCKER_DATA_PATH:/var/lib/docker \
        -v $APP_PATH:/app \
        $IMAGE_NAME >> $LOG_FILE 2>&1
    if [ $? -ne 0 ]; then
        log_message "Fehler beim Starten des Containers."
        exit 1
    fi
    docker ps | grep $CONTAINER_NAME > /dev/null
    if [ $? -ne 0 ]; then
        log_message "Fehler: Der Container $CONTAINER_NAME läuft nicht. Überprüfe die Logs."
        exit 1
    fi
    log_message "Docker-Container erfolgreich gestartet: $CONTAINER_NAME"
}

# Docker-Logs anzeigen
show_logs() {
    log_message "Starte Logs für den Container $CONTAINER_NAME (Abbruch mit Ctrl+C möglich)..."
    docker logs -f $CONTAINER_NAME
}

# Interaktive Konsole starten
open_console() {
    log_message "Wechsel in die Docker-Konsole des Containers..."
    docker exec -it $CONTAINER_NAME /bin/bash
}

# Hauptablauf
log_message "Start: Bereinigung, Build und Start von Docker."
verify_docker_storage
cleanup_temp_files
cleanup_docker
build_container
stop_and_remove_container
start_container

# Logs anzeigen oder interaktive Konsole betreten
while true; do
    read -p "Option auswählen (1=Logs anzeigen, 2=In Docker-Shell wechseln): " OPTION
    case $OPTION in
        1)
            show_logs
            break
            ;;
        2)
            open_console
            break
            ;;
        *)
            log_message "Ungültige Option. Bitte erneut versuchen."
            ;;
    esac
done
