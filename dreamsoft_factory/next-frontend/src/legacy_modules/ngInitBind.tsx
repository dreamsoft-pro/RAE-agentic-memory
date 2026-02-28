/**
 * Service: ngInitBind
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useEffect, useState } from 'react';
import { useRef } from 'react';
import { render } from '@testing-library/react';
import { compile } from 'angular-compile';

const NgInitBind: React.FC<{ ngBindHtml?: string }> = ({ ngBindHtml }) => {
  const elementRef = useRef(null);
  const [content, setContent] = useState('');

  useEffect(() => {
    if (ngBindHtml && elementRef.current) {
      const compiledContent = compile(ngBindHtml)({});
      setContent(compiledContent);
    }
  }, [ngBindHtml]);

  return <div ref={elementRef}>{content}</div>;
};

export default NgInitBind;
