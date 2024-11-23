# Verwende ein Node.js-Image als Basis
FROM node:20

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Installiere System-Tools, SQLite und benötigte Bibliotheken
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
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Zeitzone auf "Europe/Berlin" einstellen
RUN ln -sf /usr/share/zoneinfo/Europe/Berlin /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Erstelle eine virtuelle Python-Umgebung und installiere Python-Abhängigkeiten
COPY requirements.txt .
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip setuptools wheel && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt || \
    /opt/venv/bin/pip install --no-cache-dir git+https://github.com/bukosabino/ta

# Setze die virtuelle Umgebung als Standard für Python
ENV PATH="/opt/venv/bin:$PATH"

# Kopiere Python-Skripte
COPY database.py /app
COPY trading_logic.py /app
COPY process_all_pairs.py /app

# Kopiere `package.json` und installiere Node.js-Abhängigkeiten
COPY package*.json ./ 
RUN npm install -g npm@latest
RUN npm install
RUN npm install express

# Füge den restlichen Projektinhalt hinzu
COPY . .

# Setze Schreibrechte für das Arbeitsverzeichnis
RUN chmod -R 777 /app

# Erstelle Log-Verzeichnis und setze Berechtigungen
RUN mkdir -p /app/logs && chmod -R 777 /app/logs

# Füge das Log-Clear-Skript hinzu und konfiguriere den Cron-Job
COPY clear_logs.sh /usr/local/bin/clear_logs.sh
RUN chmod +x /usr/local/bin/clear_logs.sh
RUN echo "0 0 1 */2 * /bin/bash /usr/local/bin/clear_logs.sh" > /etc/cron.d/clear_logs
RUN chmod 0644 /etc/cron.d/clear_logs

# Exponiere den Standardport der Anwendung
EXPOSE 3000

# Starte Node.js und Python parallel mit Logging
CMD ["sh", "-c", "node index.js & python3 process_all_pairs.py & tail -f /dev/null"]
