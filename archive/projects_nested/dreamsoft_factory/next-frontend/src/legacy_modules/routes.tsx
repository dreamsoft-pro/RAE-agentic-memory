/**
 * Service: routes
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

/**
 */

export interface RouteConfig {
  path: string;
  name: string;
  component: string;
  authRequired?: boolean;
  layout?: 'default' | 'auth' | 'calculator';
}

export const APP_ROUTES: RouteConfig[] = [
  {
    path: '/',
    name: 'home',
    component: '@/views/Home',
    layout: 'default'
  },
  {
    path: '/calc',
    name: 'calculator',
    component: '@/views/Calculator',
    layout: 'calculator'
  },
  {
    path: '/cart',
    name: 'cart',
    component: '@/views/Cart',
    layout: 'default'
  },
  {
    path: '/login',
    name: 'login',
    component: '@/views/Auth/Login',
    layout: 'auth'
  },
  {
    path: '/register',
    name: 'register',
    component: '@/views/Auth/Register',
    layout: 'auth'
  },
  {
    path: '/client-zone',
    name: 'clientZone',
    component: '@/views/ClientZone',
    authRequired: true,
    layout: 'default'
  },
  {
    path: '/orders',
    name: 'orders',
    component: '@/views/Orders',
    authRequired: true,
    layout: 'default'
  }
];

/**
 */
export const getRoute = (name: string) => APP_ROUTES.find(r => r.name === name);

/**
 */
export const getStaticPaths = () => APP_ROUTES.map(r => r.path);
