var express = require('express');
var app = express();
var serveStatic = require('serve-static')
const rendertron = require("rendertron-middleware")

const BOT_UA_PATTERN = new RegExp(
    'Googlebot|Bingbot|Yahoo|DuckDuckBot|Twitterbot|FacebookExternalHit|LinkedInBot|Pinterest|Slackbot|WhatsApp'
);

const rendertronUrl = process.env.rendertronUrl

if (rendertronUrl !== undefined) {
    app.use(rendertron.makeMiddleware({
        proxyUrl: rendertronUrl,
        userAgentPattern: BOT_UA_PATTERN
    }))
}

app.use(serveStatic('dist'));
module.exports = app;
