/**
 * Service: 10
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Props {
  currentType: { names: { [key: string]: string } };
  currentLang: { code: string };
}

const ProductView: React.FC<Props> = ({ currentType, currentLang }) => (
  <div className="container" id="container-product">
    <div className="row" id="row-product-description">
      <div className="col-xs-12">
        <h1 className="page-header">{currentType.names[currentLang.code]}</h1>
        {/* This will be replaced by the content of description.html */}
      </div>
    </div>
    <div className="row">
      <div className="col-md-8 col-sm-12 col-xs-12">
        <div className="row">
          <div className="col-sm-5">
            {/* This will be replaced by the content of thumbnails.html */}
            {/* This will be replaced by the content of menu.html */}
          </div>
          <div className="col-sm-7">
            {/* This will be replaced by the content of parameters.html */}
            {/* This will be replaced by the content of patterns.html */}
          </div>
        </div>
        <div className="row">
          <div className="col-xs-12">
            {/* This will be replaced by the content of delivery.html */}
          </div>
        </div>
      </div>
      <div className="col-md-4 col-xs-12">
        <div className="row">
          <div className="col-xs-12 col-sm-6 col-md-12">
            {/* This will be replaced by the content of galleries.html */}
          </div>
          <div className="col-xs-12 col-sm-6 col-md-12">
            {/* This will be replaced by the content of configuration.html */}
          </div>
        </div>
      </div>
    </div>
  </div>
);

export default ProductView;