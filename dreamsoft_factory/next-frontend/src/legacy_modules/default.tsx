/**
 * Service: default
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const ProductView: React.FC = () => {
    return (
        <div className="container containerCalc" id="container-product">
            <div className="row" id="row-product-description">
                <div className="col-xs-12">
                    <h1 className="page-header">{currentType.names[currentLang.code]}</h1>
                    {/* This will be replaced by the content of description.html */}
                    {/* <!-- /build --> */}
                </div>
            </div>
            <div ng-if="!emptyProduct" className="row">
                <div className="col-md-8">
                    <div className="row">
                        <div className="col-md-6">
                            {/* This will be replaced by the content of parameters.html */}
                            {/* <!-- build:include ../panels/parameters.html --> */}
                        </div>
                        <div className="col-md-6">
                            {/* This will be replaced by the content of realization.html */}
                            {/* <!-- build:include ../panels/realization.html --> */}
                        </div>
                        <div className="col-md-12">
                            {/* This will be replaced by the content of delivery.html */}
                            {/* <!-- build:include ../panels/delivery.html --> */}
                        </div>
                    </div>
                </div>
                <div className="col-md-4">
                    {/* This will be replaced by the content of summary.html */}
                    {/* <!-- build:include ../panels/summary.html --> */}
                    {/* This will be replaced by the content of configuration.html */}
                    {/* <!-- build:include ../panels/configuration.html --> */}
                </div>
            </div>
        </div>
    );
};

export default ProductView;