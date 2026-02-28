/**
 * Service: RootLayout
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { CalculatorProvider } from './Calculator/CalculatorContext';
import { CartProvider } from './CartContext';

/**
 */

export const RootLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <CartProvider>
      <CalculatorProvider>
        <div className="min-h-screen bg-white font-sans text-slate-900">
          {/* Header */}
          <nav className="border-b border-slate-200 bg-white sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
              <div className="flex justify-between h-16 items-center">
                <div className="flex-shrink-0 flex items-center">
                  <span className="text-xl font-bold tracking-tight text-blue-600">DREAMSOFT<span className="text-slate-400">PRO 2.0</span></span>
                </div>
                <div className="hidden md:ml-6 md:flex md:space-x-8">
                  <a href="#" className="text-slate-500 hover:text-slate-900 px-3 py-2 text-sm font-medium">Calculator</a>
                  <a href="#" className="text-slate-500 hover:text-slate-900 px-3 py-2 text-sm font-medium">Cart</a>
                  <a href="#" className="text-slate-500 hover:text-slate-900 px-3 py-2 text-sm font-medium">Orders</a>
                </div>
              </div>
            </div>
          </nav>

          {/* Page Content */}
          <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            {children}
          </div>

          {/* Footer */}
          <footer className="bg-slate-50 border-t border-slate-200 mt-auto">
            <div className="max-w-7xl mx-auto py-6 px-4 overflow-hidden sm:px-6 lg:px-8">
              <p className="text-center text-slate-400 text-sm">
                &copy; 2026 Dreamsoft. Modernized by RAE-Feniks System.
              </p>
            </div>
          </footer>
        </div>
      </CalculatorProvider>
    </CartProvider>
  );
};
