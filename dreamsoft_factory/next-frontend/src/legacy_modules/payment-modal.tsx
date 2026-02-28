/**
 * Service: payment-modal
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

To modernize the provided HTML file and convert it to TypeScript with JSX syntax, we need to follow a few steps. First, let's ensure that the structure is clear and follows best practices for React components. Then, we will use TypeScript for type-checking and better development experience. Finally, we will integrate JSX for rendering UI elements in a more flexible way compared to HTML.

Here's how you can convert the provided HTML into a modern TypeScript with JSX format:

import React from 'react';

interface Order {
    paid: number;
    orderNumber: string;
    created: string;
    products: Array<{
        names: {[key: string]: string};
        name: string;
        price: number;
        grossPrice: number;
        calcProducts: Array<{ formatName?: string, typeName?: string }>;
        volume: number;
    }>;
    sumGrossPrice: number;
    deliveryGrossPrice: number;
    totalPrice: number;
    totalGrossPrice: number;
    currency: string;
}

interface Payment {
    ID: number;
    names: {[key: string]: string};
    contents: {[key: string]: string};
    limitExceeded: boolean;
    infoFor