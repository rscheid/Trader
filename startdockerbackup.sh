#!/bin/bash

# Setze Variablen
IMAGE_NAME="trading_bot_image"
CONTAINER_NAME="trading_bot_container"
DOCKERFILE_PATH="."  # Pfad zum Dockerfile (Standard: aktuelles Verzeichnis)

echo "=== Docker-Image bauen ==="
docker build -t $IMAGE_NAME $DOCKERFILE_PATH
if [ $? -ne 0 ]; then
    echo "Fehler beim Bauen des Docker-Images. Abbruch!"
    exit 1
fi

echo "=== Laufenden Container stoppen ==="
docker stop $CONTAINER_NAME 2>/dev/null || echo "Kein laufender Container gefunden."

echo "=== Container löschen ==="
docker rm $CONTAINER_NAME 2>/dev/null || echo "Kein Container zum Löschen gefunden."

echo "=== Neuen Container starten ==="
docker run --name $CONTAINER_NAME -d $IMAGE_NAME
if [ $? -eq 0 ]; then
    echo "Container erfolgreich gestartet: $CONTAINER_NAME"
else
    echo "Fehler beim Starten des Containers."
    exit 1
fi
