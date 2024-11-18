# Verwende ein Node.js-Image als Basis
FROM node:20

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere System-Tools und Bibliotheken für Python und Pandas
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    gcc \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Erstelle eine virtuelle Python-Umgebung und installiere Python-Abhängigkeiten
COPY requirements.txt .
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel && \
    /opt/venv/bin/pip install --only-binary=:all: --no-cache-dir -r requirements.txt

# Setze die virtuelle Umgebung als Standard für Python
ENV PATH="/opt/venv/bin:$PATH"

# Kopiere das Python-Skript
COPY rsi_strategy.py .

# Kopiere `package.json` und `package-lock.json`, wenn vorhanden, und installiere Node.js-Abhängigkeiten
COPY package*.json ./
RUN npm install

# Kopiere den restlichen Projektinhalt
COPY . .

# Setze Schreibrechte für das Arbeitsverzeichnis
RUN chmod -R 777 /app

# Exponiere den Standardport der Anwendung
EXPOSE 3000

# Startbefehl für den Node.js-Server
CMD ["npm", "start"]
