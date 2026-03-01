/**
 * Service: systemjs.config
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

/**
 * Next.js uses native ES modules and automated bundling.
 */
export const legacyModules = {
    'npm:': 'node_modules/',
    'app': 'src',
    '@angular': 'node_modules/@angular',
    'rxjs': 'node_modules/rxjs'
};
