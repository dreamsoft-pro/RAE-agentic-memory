javascript
const express = require('@lib/api/express');
const serveStatic = require('serve-static');
const rendertron = require("rendertron-middleware");

// [BACKEND_ADVICE] Define bot user agent pattern.
const BOT_UA_PATTERN = new RegExp(
    'Googlebot|Bingbot|Yahoo|DuckDuckBot|Twitterbot|FacebookExternalHit|LinkedInBot|Pinterest|Slackbot|WhatsApp'
);

// [BACKEND_ADvice] Check and apply rendertron middleware if rendertronUrl is defined.
const rendertronUrl = process.env.RENDERTRON_URL;
if (rendertronUrl !== undefined) {
    const middleware = rendertron.makeMiddleware({
        proxyUrl: rendertronUrl,
        userAgentPattern: BOT_UA_PATTERN
    });
    app.use(middleware);
}

// [BACKEND_ADVICE] Serve static files from 'dist' directory.
app.use(serveStatic('dist'));

module.exports = app;
