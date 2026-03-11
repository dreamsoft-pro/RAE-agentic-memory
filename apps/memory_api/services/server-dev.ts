javascript
const express = require('express');
const { serveStatic } = require('serve-static');
const rendertron = require("rendertron-middleware");
const api = require('@/lib/api');

const BOT_UA_PATTERN = new RegExp(
    'Googlebot|Bingbot|Yahoo|DuckDuckBot|Twitterbot|FacebookExternalHit|LinkedInBot|Pinterest|Slackbot|WhatsApp'
);

const rendertronUrl = process.env.rendertronUrl || "";

if (rendertronUrl.length) {
    app.use(rendertron.makeMiddleware({
        proxyUrl: rendertronUrl,
        userAgentPattern: BOT_UA_PATTERN,
        timeout: 50000, // large timeout due to laptop performance
    }));
}

app.use(serveStatic('app'));
app.use(serveStatic('dist'));

// [BACKEND_ADVICE] Add a route for API calls if necessary.
app.get('/api/*', api.handleApiRequest);

app.use('/*', (req, res) => {
  res.sendFile(__dirname + '/app/index.html');
});

module.exports = app;
