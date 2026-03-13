/**
 * Service: unidruk
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import '../styles/unidruk.css'; // Assuming you have a CSS file for styling

interface Props {
  currentType: { names: { [key: string]: string } };
  currentLang: { code: string };
}

const Unidruk: React.FC<Props> = ({ currentType, currentLang }) => {
  return (
    <div className="container" id="container-product">
      <div className="row" id="row-product-description">
        <div className="col-xs-12">
          <h1 className="page-header">{currentType.names[currentLang.code]}</h1>
        </div>
      </div>
      <div className="row">
        <div className="col-md-3">
          {/* build:include ../panels/menu.html */}
          This will be replaced by the content of menu.html
          {/* /build */}
        </div>
        <div className="col-md-9">
          <div className="row">
            <div className="col-md-7">
              {/* build:include ../panels/patterns-thumbnails.html */}
              This will be replaced by the content of patterns.html
              {/* /build */}
            </div>
            <div className="col-md-5">
              {/* build:include ../panels/galleries.html */}
              This will be replaced by the content of galleries.html
              {/* /build */}
            </div>
          </div>
          <div className="row">
            <div className="col-md-7">
              {/* build:include ../panels/parameters.html */}
              This will be replaced by the content of parameters.html
              {/* /build */}
            </div>
            <div className="col-md-5">
              {/* build:include ../panels/realization.html */}
              This will be replaced by the content of realization.html
              {/* /build */}
            </div>
          </div>
          <div className="row">
            <div className="col-md-12">
              {/* build:include ../panels/delivery.html */}
              This will be replaced by the content of delivery.html
              {/* /build */}
            </div>
          </div>
          <div className="row">
            <div className="col-md-7">
              {/* build:include ../panels/card-guide.html */}
              This will be replaced by the content of description.html
              {/* /build */}
            </div>
            <div className="col-md-5">
              {/* build:include ../panels/configuration.html */}
              This will be replaced by the content of configuration.html
              {/* /build */}
              {/* build:include ../panels/summary.html */}
              This will be replaced by the content of summary.html
              {/* /build */}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Unidruk;