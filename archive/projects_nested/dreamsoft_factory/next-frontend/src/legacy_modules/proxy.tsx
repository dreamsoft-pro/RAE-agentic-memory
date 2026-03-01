/**
 * Service: proxy
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import http from 'http';
import httpProxy from 'http-proxy';

const proxy = httpProxy.createProxyServer({});

const server = http.createServer((req, res) => {
    const options = {
        target: 'http://localhost:9001',
        secure: false,
        ws: false,
        prependPath: false,
        ignorePath: false,
    };

    const url = require('url').parse(req.url);

    switch (url.pathname) {
        case '/35/images/favicon.ico':
            req.url = '/favicon.ico';
            break;
        case '/templates/default/1/footer.html':
            // Handle the footer template request if needed
            break;
        default:
            proxy.web(req, res, options);
    }
});

server.listen(8080, () => {
    console.log('Server is running on http://localhost:8080');
});