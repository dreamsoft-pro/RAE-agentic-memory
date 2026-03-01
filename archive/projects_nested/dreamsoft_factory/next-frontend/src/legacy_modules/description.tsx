/**
 * Service: description
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Description {
  langs: { [key: string]: { name: string; description: string } };
  order: number;
}

interface Props {
  descriptions: Description[];
  currentLang: { code: string };
}

const ProductDescription: React.FC<Props> = ({ descriptions, currentLang }) => {
  return (
    <div className="panel panel-default panel-product-description">
      {descriptions
        .filter(desc => Object.keys(desc.langs).length > 0)
        .sort((a, b) => a.order - b.order)
        .map((description, index) => (
          <div className="panel-heading" key={index}>
            <h3 className="panel-title">{description.langs[currentLang.code].name}</h3>
          </div>
        ))}
      {descriptions
        .filter(desc => Object.keys(desc.langs).length > 0)
        .sort((a, b) => a.order - b.order)
        .map((description, index) => (
          <div className="panel-body" key={index}>
            {description.langs[currentLang.code].description}
          </div>
        ))}
    </div>
  );
};

export default ProductDescription;