#!/bin/bash

# Skript: upload.sh
# Beschreibung: Lädt alle Dateien vom Server auf das GitHub-Repository hoch und erzwingt das Hochladen bei Konflikten.

# Prüfen, ob sich das Skript im Git-Repository befindet
if [ ! -d .git ]; then
  echo "Dieses Verzeichnis ist kein Git-Repository. Bitte in ein Git-Repository wechseln."
  exit 1
fi

# Alle Änderungen zum Commit vorbereiten
echo "Staging alle Dateien..."
git add -A

# Commit mit einer Standardnachricht
echo "Commit mit Standardnachricht..."
git commit -m "Automatischer Upload vom Server"

# Remote-Änderungen einholen, falls Konflikte bestehen
echo "Pullen der neuesten Änderungen vom Remote-Repository..."
git pull --rebase

# Änderungen pushen
echo "Pushen der Änderungen ins Remote-Repository..."
git push origin main

# Erfolgsmeldung
if [ $? -eq 0 ]; then
  echo "Alle Änderungen erfolgreich auf GitHub hochgeladen!"
else
  echo "Fehler beim Hochladen. Bitte prüfen."
fi
