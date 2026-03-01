/**
 * Service: help
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

const HelpPage = () => {
  const { t } = useTranslation();

  return (
    <div className="container" id="content-pricelist">
      <div className="row">
        <div className="col-xs-12">
          <h1 className="page-header ng-binding">{t('help')}</h1>
        </div>
      </div>
      <div className="row">
        <div className="col-md-12">
          <div className="staticContentBox" dangerouslySetInnerHTML={{ __html: t('static.help') }} />
        </div>
      </div>
    </div>
  );
};

export default HelpPage;