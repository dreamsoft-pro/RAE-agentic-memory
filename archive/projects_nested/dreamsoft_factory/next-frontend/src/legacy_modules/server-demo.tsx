/**
 * Service: server-demo
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import express from 'express';
import path from 'path';

const app = express();
const port = 3000; // You can set the port number as needed

app.use(express.static('app'));

app.use('/*', (req, res) => {
  res.sendFile(path.join(__dirname, 'app/demo/index.html'));
});

app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});

export default app;
