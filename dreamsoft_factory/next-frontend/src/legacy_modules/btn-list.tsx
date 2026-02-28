/**
 * Service: btn-list
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface BtnListProps {
  items: any[];
  labelFn?: (item: any) => string;
  compareFn: (item: any, model: any) => boolean;
  clickFn: (item: any, model: any) => void;
  overallClasses?: string;
  model: any;
}

const BtnList: React.FC<BtnListProps> = ({ items, labelFn, compareFn, clickFn, overallClasses, model }) => {
  return (
    <div className="btn-list">
      {items.map((item, index) => (
        <button
          key={index}
          className={`${overallClasses} custom-list-view list-group-item class-custom-select-box ${compareFn(item, model) ? 'list-group-item-info' : ''}`}
          onClick={() => clickFn(item, model)}
        >
          {labelFn ? labelFn(item) : item.name}
        </button>
      ))}
    </div>
  );
};

export default BtnList;
