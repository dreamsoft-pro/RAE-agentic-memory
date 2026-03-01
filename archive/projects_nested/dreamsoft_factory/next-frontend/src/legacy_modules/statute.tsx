/**
 * Service: statute
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

const Statute: React.FC = () => {
  const { t } = useTranslation();

  return (
    <div className="container" id="content-statute">
      <div className="row">
        <div className="col-xs-12">
          <h1 className="page-header ng-binding">{t('statute')}</h1>
        </div>
      </div>
      <div className="row">
        <div className="col-md-12">
          <div className="staticContentBox" data-content="static.statute"></div>
        </div>
      </div>
    </div>
  );
};

export default Statute;