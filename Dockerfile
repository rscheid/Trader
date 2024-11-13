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
CMD ["npm", "start"]
