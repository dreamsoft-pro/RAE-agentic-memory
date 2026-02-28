/**
 * Service: lang-conditional
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';

const LangConditional: React.FC<{ langKey: string }> = ({ langKey }) => {
  const { t } = useTranslation();
  const [content, setContent] = useState('');

  useEffect(() => {
    const translation = t(langKey);
    if (!translation || translation === langKey) {
      return;
    }
    setContent(translation);
  }, [langKey, t]);

  return content ? <div>{content}</div> : null;
};

export default LangConditional;