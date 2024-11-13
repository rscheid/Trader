const express = require('express');
const app = express();
const PORT = 3000;

app.get('/', (req, res) => {
  res.send('Hello from Trading Server Binance!');
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});