# Verwende ein Node.js-Image als Basis
FROM node:20

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere Python3, Pip und venv
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Erstelle eine virtuelle Python-Umgebung und installiere Python-Abhängigkeiten
COPY requirements.txt .
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Setze die virtuelle Umgebung als Standard für Python
ENV PATH="/opt/venv/bin:$PATH"

# Kopiere das Python-Skript
COPY rsi_strategy.py .

# Kopiere `package.json` und `package-lock.json`, wenn vorhanden, und installiere Node.js-Abhängigkeiten
COPY package*.json ./
RUN npm install

# Kopiere den restlichen Projektinhalt
COPY . .

# Exponiere den Standardport der Anwendung
EXPOSE 3000

# Startbefehl für den Node.js-Server
CMD ["npm", "start"]
