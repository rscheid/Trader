# Verwende ein Python-Image als Basis
FROM python:3.10-slim

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die Abhängigkeitsdatei in den Container
COPY requirements.txt .

# Aktualisiere pip und installiere System-Tools sowie Abhängigkeiten
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Kopiere den gesamten Projektinhalt in den Container
COPY . .

# Setze Schreibrechte für das Arbeitsverzeichnis
RUN chmod -R 777 /app

# Exponiere einen Standardport (optional, falls später benötigt, z. B. für APIs)
EXPOSE 8000

# Starte das Skript und halte den Container offen
CMD ["sh", "-c", "python3 train_model.py && tail -f /dev/null"]
