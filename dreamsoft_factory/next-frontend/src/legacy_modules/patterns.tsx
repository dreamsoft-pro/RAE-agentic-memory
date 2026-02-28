/**
 * Service: patterns
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

interface Pattern {
  patternFile: string;
  patternIcon: string;
}

interface Props {
  patterns: Pattern[];
}

const Patterns: React.FC<Props> = ({ patterns }) => {
  const { t } = useTranslation();

  return (
    <div className="panel panel-default" id="panel-product-patterns">
      {patterns.length > 0 && (
        <>
          <div className="panel-heading">
            <h3 className="panel-title">{t('models')}</h3>
          </div>
          <div className="panel-body">
            <ul className="list-inline">
              {patterns.filter(pattern => pattern.patternFile && pattern.patternIcon).map((pattern, index) => (
                <li key={index}>
                  <a href={pattern.patternFile} target="_blank" rel="noopener noreferrer">
                    <img loading="lazy" src={pattern.patternIcon} alt="Pattern" />
                  </a>
                </li>
              ))}
            </ul>
          </div>
        </>
      )}
    </div>
  );
};

export default Patterns;