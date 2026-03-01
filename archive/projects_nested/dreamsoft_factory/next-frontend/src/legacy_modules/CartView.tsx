/**
 * Service: CartView
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { CartProvider } from './CartContext';
import { _stitched as CartLogic } from './cart_Atomic/_stitched';
import { _stitched as CartWidget } from './CartWidgetService_Atomic/_stitched';

/**
 * CartView.tsx
 * Orchestrates shopping cart modules.
 */

export const CartView: React.FC = () => {
  return (
    <CartProvider>
      <div className="cart-page bg-white p-6">
        <h1 className="text-3xl font-bold mb-8">Your Shopping Cart</h1>
        <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">
          <div className="xl:col-span-8">
            {/* Logic and item list */}
            {/* @ts-ignore - Stitched legacy logic */}
            <CartLogic />
          </div>
          <div className="xl:col-span-4">
            {/* Summary and widgets */}
            {/* @ts-ignore - Stitched legacy widget */}
            <CartWidget />
          </div>
        </div>
      </div>
    </CartProvider>
  );
};
