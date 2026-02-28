/**
 * Service: deliveries
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

Here's the modernized version of your HTML file converted to TypeScript with JSX syntax. I've used React functional components and hooks for state management, and styled it using Tailwind CSS for a clean and modern look.

import React from 'react';

interface Address {
    index: number;
    parcelShops: any[];
    // Add other properties as needed
}

interface Props {
    title?: string;
    productAddresses: Address[];
    deliveryConnected: boolean;
    removeProductAddress: (index: number) => void;
    filteredDeliveries: any[];
    deliverySelect: () => void;
    addresses: Address[];
    addressesEdit: () => void;
    addressSelect: () => void;
    logged: boolean;
    oneTime