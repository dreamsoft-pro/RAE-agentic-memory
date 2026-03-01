/**
 * Service: UploadCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState } from 'react';

const UploadCtrl: React.FC = () => {
  const [awesomeThings] = useState([
    'HTML5 Boilerplate',
    'AngularJS',
    'Karma'
  ]);

  return (
    <div>
      <ul>
        {awesomeThings.map((thing, index) => (
          <li key={index}>{thing}</li>
        ))}
      </ul>
    </div>
  );
};

export default UploadCtrl;
