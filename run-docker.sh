#!/bin/bash

# Variablen
IMAGE_NAME="trading_bot_image"
CONTAINER_NAME="trading_bot_container"
DOCKERFILE_PATH="Dockerfile"
PORT_MAPPING="3000:3000"
LOG_FILE="run_docker.log"


# Setze lokale Zeitzone
docker run -dit \
  --name $CONTAINER_NAME \
  -v /etc/localtime:/etc/localtime:ro \
  -v /etc/timezone:/etc/timezone:ro \
  -p $PORT_MAPPING \
  $IMAGE_NAME


# Funktion: Nachricht mit Zeitstempel loggen
log_message() {
    local MESSAGE=$1
    echo "$(date +"%Y-%m-%d %H:%M:%S") - $MESSAGE" | tee -a $LOG_FILE
}

# Funktion: Docker-Image bauen
build_image() {
    log_message "Starte Docker-Build mit Dockerfile: $DOCKERFILE_PATH"
    if docker build -f $DOCKERFILE_PATH -t $IMAGE_NAME . >> $LOG_FILE 2>&1; then
        log_message "Docker-Image erfolgreich erstellt: $IMAGE_NAME"
    else
        log_message "FEHLER: Docker-Build fehlgeschlagen. Überprüfe die Logs unter $LOG_FILE."
        exit 1
    fi
}

# Funktion: Vorherigen Container stoppen und entfernen
stop_and_remove_container() {
    log_message "Prüfe auf laufende Container mit dem Namen: $CONTAINER_NAME"
    if [ "$(docker ps -q -f name=$CONTAINER_NAME)" ]; then
        log_message "Stoppe laufenden Container: $CONTAINER_NAME"
        docker stop $CONTAINER_NAME >> $LOG_FILE 2>&1
    fi
    if [ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]; then
        log_message "Entferne bestehenden Container: $CONTAINER_NAME"
        docker rm $CONTAINER_NAME >> $LOG_FILE 2>&1
    fi
}

# Funktion: Docker-Container starten
start_container() {
    log_message "Starte neuen Docker-Container mit dem Namen: $CONTAINER_NAME"
    if docker run -dit --name $CONTAINER_NAME -p $PORT_MAPPING $IMAGE_NAME >> $LOG_FILE 2>&1; then
        log_message "Docker-Container erfolgreich gestartet: $CONTAINER_NAME"
    else
        log_message "FEHLER: Container konnte nicht gestartet werden."
        exit 1
    fi
}

# Funktion: Docker-Logs anzeigen
show_logs() {
    log_message "Starte Logs des Containers $CONTAINER_NAME (Abbruch mit Ctrl+C möglich)..."
    docker logs -f $CONTAINER_NAME
}

# Funktion: Interaktive Konsole öffnen
open_console() {
    log_message "Wechsel in die Docker-Konsole des Containers..."
    docker exec -it $CONTAINER_NAME /bin/bash
}

# Hauptablauf
log_message "Starte Skript: Docker-Build und Container-Management."
build_image
stop_and_remove_container
start_container

# Optionen nach Start
while true; do
    echo "Option auswählen: (1=Logs anzeigen, 2=In Docker-Shell wechseln, 3=Beenden)"
    read -p "Option: " OPTION
    case $OPTION in
        1)
            show_logs
            ;;
        2)
            open_console
            ;;
        3)
            log_message "Skript beendet."
            exit 0
            ;;
        *)
            echo "Ungültige Option. Bitte erneut versuchen."
            ;;
    esac
done
