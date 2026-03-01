/**
 * Service: card-guide
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useEffect, useState } from 'react';
import { parse } from 'marked';

const CardGuide = ({ currentType }) => {
  const [content, setContent] = useState('');

  useEffect(() => {
    if (currentType && currentType.cardGuide) {
      const parsedContent = parse(currentType.cardGuide);
      setContent(parsedContent);
    }
  }, [currentType]);

  return (
    <div className="panel panel-default" style={{ display: currentType.cardGuide ? 'block' : 'none' }}>
      <div className="panel-heading">
        <h3 className="panel-title">Opis produktu</h3>
      </div>
      <div className="panel-body" dangerouslySetInnerHTML={{ __html: content }} />
    </div>
  );
};

export default CardGuide;