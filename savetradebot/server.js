const express = require('express');
const { exec } = require('child_process');
const app = express();
const PORT = 3000;

// Endpunkt für das RSI-Signal
app.get('/rsi', (req, res) => {
    // Prüfen und ausgeben, aus welchem Verzeichnis das Python-Skript läuft
    exec('pwd', (err, stdout, stderr) => {
        console.log(`Working directory: ${stdout.trim()}`);
    });

    // Python-Skript ausführen
    exec('python3 rsi_strategy.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            console.error(`Details: ${stderr}`);
            return res.status(500).send(`Error running RSI strategy: ${stderr}`);
        }
        res.send(stdout); // Ergebnis des Skripts zurückgeben
    });
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
