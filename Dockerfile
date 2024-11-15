# Base Image für Python
FROM python:3.9-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Python und Pip installieren
RUN apt-get update && apt-get install -y python3 python3-pip

# Dependencies installieren
COPY requirements.txt .

# Sicherstellen, dass ccxt für Python3 installiert wird
RUN pip3 install --no-cache-dir -r requirements.txt

# Kopiere die Datei `rsi_strategy.py`
COPY rsi_strategy.py .

# Standard-Befehl: Testlauf für die RSI-Strategie
CMD ["python", "rsi_strategy.py"]

# Verwende Node.js 20 als Basis
FROM node:20

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere `package.json` und `package-lock.json`, wenn vorhanden, und installiere Abhängigkeiten
COPY package*.json ./
RUN npm install

# Kopiere den restlichen Projektinhalt
COPY . .

# Exponiere den Standardport der Anwendung
EXPOSE 3000

# Befehl zum Starten der Anwendung
# CMD ["node", "-e", "console.log('Server-Test erfolgreich!'); process.exit(0);"]
CMD ["npm", "start"]
