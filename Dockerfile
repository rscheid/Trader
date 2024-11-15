# Verwende ein Node.js-Image als Basis und installiere Python zusätzlich
FROM node:20

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere Python3 und Pip3
RUN apt-get update && apt-get install -y python3 python3-pip

# Kopiere und installiere Python-Abhängigkeiten
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Kopiere das Python-Skript
COPY rsi_strategy.py .

# Kopiere `package.json` und `package-lock.json`, wenn vorhanden, und installiere Node.js-Abhängigkeiten
COPY package*.json ./
RUN npm install

# Kopiere den restlichen Projektinhalt
COPY . .

# Exponiere den Standardport der Anwendung
EXPOSE 3000

# Befehl zum Starten der Node.js-Anwendung
CMD ["npm", "start"]
