var express = require('express');
var app = express();
var serveStatic = require('serve-static')
const rendertron = require("rendertron-middleware")

app.use(serveStatic('app'));
app.use(serveStatic('dist'));

const BOT_UA_PATTERN = new RegExp(
    'Googlebot|Bingbot|Yahoo|DuckDuckBot|Twitterbot|FacebookExternalHit|LinkedInBot|Pinterest|Slackbot|WhatsApp'
);

const rendertronUrl = process.env.rendertronUrl || "";

if (rendertronUrl.length) {
    app.use(rendertron.makeMiddleware({
        proxyUrl: rendertronUrl,
        userAgentPattern: BOT_UA_PATTERN,
        // duży timeout bo laptop nie wyrabia
        timeout: 50000,
    }));
}

app.use('/*', function(req, res){
  res.sendFile(__dirname + '/app/index.html');
});

module.exports = app;
