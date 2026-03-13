/**
 * Service: webpack.config
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import webpack from 'webpack';
import dotenv from 'dotenv';

// Load the .env file
const env = dotenv.config().parsed;

// Prepare the variables to be injected into the application
const envKeys = Object.keys(env).reduce((prev, next) => {
    prev[`process.env.${next}`] = JSON.stringify(env[next]);
    return prev;
}, {});

export default {
    plugins: [
        new webpack.DefinePlugin(envKeys)
    ],
    // Next.js configurations...
};
