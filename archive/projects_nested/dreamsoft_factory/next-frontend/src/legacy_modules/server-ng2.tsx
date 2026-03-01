/**
 * Service: server-ng2
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import express from 'express';
import serveStatic from 'serve-static';
import path from 'path';

const app = express();
const port = 3000; // You can set the port number as needed

app.use(serveStatic(path.join(__dirname, 'public')));

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

export default app;
