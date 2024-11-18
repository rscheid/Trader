const express = require('express');
const { exec } = require('child_process');
const app = express();
const PORT = 3000;

// Endpoint: Führe einen Trade basierend auf RSI aus
app.get('/rsi', (req, res) => {
    const { exec } = require('child_process');
    exec('pwd', (err, stdout) => {
        console.log(`Current working directory for Python script: ${stdout}`);
    });
    exec('python3 rsi_strategy.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return res.status(500).send('Error running RSI strategy');
        }
        res.send(stdout); // Ergebnis des Scripts zurückgeben
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
