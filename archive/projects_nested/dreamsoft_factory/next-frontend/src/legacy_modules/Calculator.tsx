/**
 * Service: Calculator
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { CalculatorProvider } from './CalculatorContext';
import { Main_Functionality } from './Assembly/Main_Functionality';
import { Data_Handling_and_State_Management } from './Assembly/Data_Handling_and_State_Management';
import { UI_Components } from './Assembly/UI_Components';
import { Service_and_Utility_Functions } from './Assembly/Service_and_Utility_Functions';

/**
 */

export const CalculatorView: React.FC = () => {
  return (
    <CalculatorProvider>
      <div className="calculator-container p-4 bg-slate-50 min-h-screen">
        <header className="mb-6">
          <h1 className="text-2xl font-bold text-slate-800">Modern Calculator</h1>
        </header>
        
        <main className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Main Logic & Form Section */}
          <div className="lg:col-span-8">
            <Main_Functionality />
            <UI_Components />
          </div>
          
          {/* State & Utility Side Panels */}
          <div className="lg:col-span-4 space-y-6">
            <Data_Handling_and_State_Management />
            <Service_and_Utility_Functions />
          </div>
        </main>
        
        <footer className="mt-12 text-slate-400 text-sm">
          Powered by RAE-Feniks Modernization Engine
        </footer>
      </div>
    </CalculatorProvider>
  );
};
