# Wähle eine Basis-Node-Version
FROM node:14

# Setze das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopiere die Package-Dateien und installiere Abhängigkeiten
COPY package*.json ./
RUN npm install

# Kopiere den restlichen Code
COPY . .

# Port, auf dem die Anwendung laufen soll
EXPOSE 3000

# Befehl zum Starten der Anwendung
CMD ["npm", "start"]
