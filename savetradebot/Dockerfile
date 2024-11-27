# Stage 1: Node.js Base Image
FROM node:20 AS node-base
WORKDIR /app

# Installiere globale Node.js-Abhängigkeiten
RUN npm install -g npm@latest

# Kopiere Node.js-spezifische Dateien und installiere Abhängigkeiten
COPY package*.json ./
RUN npm install && npm install express

# Stage 2: Python Base Image
FROM python:3.10-slim AS python-base
WORKDIR /app

# Installiere System-Tools, SQLite und Bibliotheken
RUN apt-get update && apt-get install -y \
    sqlite3 \
    cron \
    tzdata \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Zeitzone auf "Europe/Berlin" einstellen
RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Erstelle virtuelle Umgebung und installiere Abhängigkeiten
COPY requirements.txt .
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt || \
    /opt/venv/bin/pip install --no-cache-dir git+https://github.com/bukosabino/ta

# Setze virtuelle Umgebung als Standard
ENV PATH="/opt/venv/bin:$PATH"

# Stage 3: Final Runtime Image
FROM python-base AS runtime
WORKDIR /app

# Kopiere Node.js-Abhängigkeiten aus node-base
COPY --from=node-base /app/node_modules ./node_modules

# Kopiere Python-Skripte
COPY database.py .
COPY trading_logic.py .
COPY process_all_pairs.py .

# Kopiere den restlichen Projektinhalt
COPY . .

# Setze Schreibrechte für das Arbeitsverzeichnis
RUN chmod -R 777 /app

# Erstelle Log-Verzeichnis und setze Berechtigungen
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Füge das Log-Clear-Skript hinzu und konfiguriere Cron-Job
COPY clear_logs.sh /usr/local/bin/clear_logs.sh
RUN chmod +x /usr/local/bin/clear_logs.sh
RUN echo "0 0 1 */2 * /bin/bash /usr/local/bin/clear_logs.sh" > /etc/cron.d/clear_logs
RUN chmod 0644 /etc/cron.d/clear_logs

# Exponiere den Standardport der Anwendung
EXPOSE 3000

# Starte Node.js und Python parallel mit Logging
CMD ["sh", "-c", "node index.js & python3 process_all_pairs.py & tail -f /dev/null"]
