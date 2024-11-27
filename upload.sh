#!/bin/bash

# Sicherstellen, dass sich das Skript im Git-Repository befindet
if [ ! -d .git ]; then
  echo "Dieses Verzeichnis ist kein Git-Repository. Bitte in ein Git-Repository wechseln."
  exit 1
fi

# Git-Remote sicherstellen
echo "Setze die Remote-URL für das Repository..."
git remote set-url origin git@github.com:rscheid/Trader.git

# Ausschließen von Verzeichnissen und spezifischen Dateien
echo "Aktualisiere .gitignore..."
cat <<EOL > .gitignore
/savetradebot/
/backups/
/root/
/any_other_directory/
/*.gz
/hall_of_fame_*.csv
/trading_bot.log
EOL

# Sicherstellen, dass .gitignore selbst hinzugefügt wird
git add .gitignore

# Dateien vorbereiten und committen
echo "Staging alle relevanten Dateien..."
git add -A

echo "Commit mit Standardnachricht..."
git commit -m "Automatischer Upload nach Bereinigung"

# Änderungen hochladen
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
