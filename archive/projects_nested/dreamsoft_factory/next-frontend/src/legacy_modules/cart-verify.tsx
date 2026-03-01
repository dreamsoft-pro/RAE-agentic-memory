/**
 * Service: cart-verify
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

interface Product {
  names: { [key: string]: string };
  name?: string;
}

interface Order {
  orderNumber: string;
  finalPrice: number;
  currency: string;
}

interface Payment {
  names: { [key: string]: string };
  contents: { [key: string]: string };
}

interface Props {
  isOnline: boolean;
  transactionConfirm: boolean;
  order: Order;
  products: Product[];
  selectedPayment: Payment;
  currentLang: { code: string };
  wasOneTime