/**
 * Service: linki
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { Link } from 'react-router-dom';

const Navigation = () => {
  return (
    <div style={{ paddingTop: '100vh' }}>
      <Link to="/deliveries">deliveries</Link>
      <Link to="/cart">cart</Link>
      <Link to="/cart_u">cart not logged</Link>
      <Link to="/calc">calc</Link>
    </div>
  );
};

export default Navigation;