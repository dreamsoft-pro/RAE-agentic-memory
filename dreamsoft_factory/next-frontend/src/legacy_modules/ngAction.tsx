/**
 * Service: ngAction
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface NgActionProps {
  ngAction?: any;
}

const NgAction: React.FC<NgActionProps> = ({ ngAction }) => {
  const [action, setAction] = React.useState(ngAction);

  React.useEffect(() => {
    if (ngAction !== action) {
      setAction(ngAction);
    }
  }, [ngAction]);

  return <div data-action={action} />;
};

export default NgAction;