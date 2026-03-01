/**
 * Service: CartContext
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { createContext, useContext, useState } from 'react';

/**
 */

interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
  metadata: any;
}

interface CartState {
  items: CartItem[];
  total: number;
  isNoRegisterMode: boolean;
}

interface CartContextType extends CartState {
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  setNoRegisterMode: (active: boolean) => void;
}

const CartContext = createContext<CartContextType | undefined>(undefined);

export const CartProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<CartState>({
    items: [],
    total: 0,
    isNoRegisterMode: false
  });

  const addItem = (item: CartItem) => {
    setState(prev => ({
      ...prev,
      items: [...prev.items, item],
      total: prev.total + item.price
    }));
  };

  const removeItem = (id: string) => {
    setState(prev => {
      const item = prev.items.find(i => i.id === id);
      return {
        ...prev,
        items: prev.items.filter(i => i.id !== id),
        total: prev.total - (item?.price || 0)
      };
    });
  };

  const value = {
    ...state,
    addItem,
    removeItem,
    setNoRegisterMode: (isNoRegisterMode: boolean) => setState(prev => ({ ...prev, isNoRegisterMode }))
  };

  return (
    <CartContext.Provider value={value}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  const context = useContext(CartContext);
  if (!context) throw new Error('useCart must be used within a CartProvider');
  return context;
};
