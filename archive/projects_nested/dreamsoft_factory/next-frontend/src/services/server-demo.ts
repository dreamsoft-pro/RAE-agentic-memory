javascript
const express = require('express');
const path = require('path');
const api = require('@lib/api');

const app = express();

// Serve static files from the 'app' directory
app.use(express.static(path.join(__dirname, 'app')));

// Fallback route to serve the demo index.html page
app.use('*', (req, res) => {
  // [BACKEND_ADVICE] Ensure fallback routes handle all possibilities.
  res.sendFile(path.join(__dirname, 'app/demo/index.html'));
});

module.exports = app;
