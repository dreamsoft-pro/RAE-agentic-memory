/**
 * Service: server-dev
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import express from 'express';
import serveStatic from 'serve-static';
import rendertron from "rendertron-middleware";
import path from 'path';

const app = express();
const BOT_UA_PATTERN = new RegExp(
    'Googlebot|Bingbot|Yahoo|DuckDuckBot|Twitterbot|FacebookExternalHit|LinkedInBot|Pinterest|Slackbot|WhatsApp'
);

const rendertronUrl = process.env.rendertronUrl || "";

if (rendertronUrl.length) {
    app.use(rendertron.makeMiddleware({
        proxyUrl: rendertronUrl,
        userAgentPattern: BOT_UA_PATTERN,
        timeout: 50000,
    }));
}

app.use(serveStatic('app'));
app.use(serveStatic('dist'));

app.use('/*', (req, res) => {
  res.sendFile(path.join(__dirname, 'app/index.html'));
});

export default app;
