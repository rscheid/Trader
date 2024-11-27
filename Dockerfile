# Python-Basisimage verwenden
FROM python:3.10-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# System-Abhängigkeiten und Julia installieren
RUN apt-get update && apt-get install -y \
    apt-utils \
    build-essential \
    wget \
    curl \
    libgmp-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Julia installieren
RUN wget https://julialang-s3.julialang.org/bin/linux/x64/1.10/julia-1.10.6-linux-x86_64.tar.gz && \
    tar -xvzf julia-1.10.6-linux-x86_64.tar.gz && \
    mv julia-1.10.6 /opt/julia && \
    ln -s /opt/julia/bin/julia /usr/local/bin/julia && \
    rm julia-1.10.6-linux-x86_64.tar.gz

# Requirements kopieren und Python-Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Projektdateien kopieren
COPY . .

# Arbeitsverzeichnisse für Logs und Daten
RUN mkdir -p /app/data /app/logs && chmod -R 777 /app

# Standardbefehl
CMD ["python3", "ai_optimizer.py"]
