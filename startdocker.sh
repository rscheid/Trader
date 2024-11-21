#!/bin/bash

# Variablen
IMAGE_NAME="trading_bot_image"
CONTAINER_NAME="trading_bot_container"
PORT_MAPPING="3000:3000"
LOG_FILE="startdocker.log"

# Funktion: Nachricht mit Zeitstempel loggen
log_message() {
    local MESSAGE=$1
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $MESSAGE" | tee -a $LOG_FILE
}

# Docker-Host bereinigen
cleanup_docker() {
    log_message "Docker bereinigen..."
    docker system prune -a --volumes -f
}

# Temporäre Dateien bereinigen
cleanup_temp_files() {
    log_message "Temporäre Dateien bereinigen..."
    find . -name "__pycache__" -type d -exec rm -rf {} +
    rm -rf *.log /tmp/*
}

# Docker-Image bauen
build_container() {
    log_message "Baue Docker-Image..."
    docker build -t $IMAGE_NAME .
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
    docker run -dit --name $CONTAINER_NAME -p $PORT_MAPPING $IMAGE_NAME
    if [ $? -ne 0 ]; then
        log_message "Fehler beim Starten des Containers."
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
cleanup_docker
cleanup_temp_files
build_container
stop_and_remove_container
start_container

# Logs anzeigen oder interaktive Konsole betreten
read -p "Option auswählen (1=Logs anzeigen, 2=In Docker-Shell wechseln): " OPTION
if [ "$OPTION" == "1" ]; then
    show_logs
elif [ "$OPTION" == "2" ]; then
    open_console
else
    log_message "Ungültige Option. Skript beendet."
fi

