/**
 * Service: server-prod
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import express from 'express';
import serveStatic from 'serve-static';
import rendertron from "rendertron-middleware";

const BOT_UA_PATTERN = new RegExp(
    'Googlebot|Bingbot|Yahoo|DuckDuckBot|Twitterbot|FacebookExternalHit|LinkedInBot|Pinterest|Slackbot|WhatsApp'
);

const rendertronUrl = process.env.rendertronUrl;

if (rendertronUrl !== undefined) {
    const app = express();
    app.use(rendertron.makeMiddleware({
        proxyUrl: rendertronUrl,
        userAgentPattern: BOT_UA_PATTERN
    }));
    app.use(serveStatic('dist'));
    module.exports = app;
} else {
    console.error("Rendertron URL is not defined.");
    process.exit(1);
}
