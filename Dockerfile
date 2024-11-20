# Verwende ein Node.js-Image als Basis
FROM node:20

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere System-Tools und SQLite
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    sqlite3 \
    apt-utils \
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
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt || \
    /opt/venv/bin/pip install --no-cache-dir git+https://github.com/bukosabino/ta

# Setze die virtuelle Umgebung als Standard für Python
ENV PATH="/opt/venv/bin:$PATH"

# Kopiere das Python-Skript
COPY rsi_strategy.py .

# Kopiere `package.json` und `package-lock.json`, wenn vorhanden, und installiere Node.js-Abhängigkeiten
COPY package*.json ./
RUN npm install

# Kopiere den restlichen Projektinhalt
COPY . .

# Installiere Cron im Docker-Image
RUN apt-get update && apt-get install -y cron

# Füge das Log-Clear-Skript in den Container ein
COPY clear_logs.sh /usr/local/bin/clear_logs.sh
RUN chmod +x /usr/local/bin/clear_logs.sh

# Füge den Cron-Job hinzu
RUN echo "0 0 1 */2 * /bin/bash /usr/local/bin/clear_logs.sh" > /etc/cron.d/clear_logs
RUN chmod 0644 /etc/cron.d/clear_logs

# Dauerhafte Zeitzoneneinstellung im Dockerfile
RUN apt-get update && apt-get install -y tzdata && \
    ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Starte den Cron-Dienst beim Container-Start
CMD cron && tail -f /dev/null

# Setze Schreibrechte für das Arbeitsverzeichnis
RUN chmod -R 777 /app

# Exponiere den Standardport der Anwendung
EXPOSE 3000

# Fallback für den Node.js-Server
# CMD ["npm", "start"]
CMD ["sh", "-c", "node index.js & python3 rsi_strategy.py"]
