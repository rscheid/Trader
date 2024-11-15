const express = require('express');
const { exec } = require('child_process');
const app = express();
const PORT = 3000;

// Endpoint: Hole RSI-Signal
app.get('/rsi', (req, res) => {
    exec('python3 rsi_strategy.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`Error executing Python script: ${error.message}`);
            return res.status(500).send('Error running RSI strategy');
        }
        if (stderr) {
            console.error(`Python script error: ${stderr}`);
            return res.status(500).send('Python script error');
        }
        res.send(stdout); // Ergebnis des Scripts zurückgeben
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on http://localhost:${PORT}`);
});
