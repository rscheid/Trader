#!/bin/bash

# Skript: upload.sh
# Beschreibung: Bereinigt Git-Caches, ignoriert bestimmte Verzeichnisse und lädt Änderungen ins Repository hoch.

# Sicherstellen, dass das aktuelle Verzeichnis ein Git-Repository ist
if [ ! -d .git ]; then
  echo "Dieses Verzeichnis ist kein Git-Repository. Bitte in ein Git-Repository wechseln."
  exit 1
fi

# Git Remote URL sicherstellen
echo "Setze die Remote-URL für das Repository..."
git remote set-url origin git@github.com:rscheid/Trader.git

# Bereinigung: Git-Cache löschen und Historie neu schreiben (optional)
echo "Bereinige Git-Cache..."
rm -rf .git/index
git clean -fdX

# Dateien und Verzeichnisse, die ignoriert werden sollen
IGNORE_DIRS=("savetradebot" "backups")
IGNORE_FILES=(".env" "trading_bot.log")

# Gitignore aktualisieren
echo "Aktualisiere .gitignore..."
for dir in "${IGNORE_DIRS[@]}"; do
  echo "/$dir/" >> .gitignore
done

for file in "${IGNORE_FILES[@]}"; do
  echo "/$file" >> .gitignore
done

# Sicherstellen, dass .gitignore hinzugefügt wird
git add .gitignore

# Dateien hinzufügen, Änderungen committen und hochladen
echo "Staging alle relevanten Dateien..."
git add -A

echo "Commit mit Standardnachricht..."
git commit -m "Automatischer Upload mit bereinigtem Cache und Ignored Files"

echo "Hole Änderungen vom Remote-Repository (Rebase)..."
git pull --rebase origin main

echo "Pushen der Änderungen ins Remote-Repository..."
git push origin main

# Erfolgsmeldung
if [ $? -eq 0 ]; then
  echo "Alle Änderungen erfolgreich auf GitHub hochgeladen!"
else
  echo "Fehler beim Hochladen. Bitte prüfen."
fi
