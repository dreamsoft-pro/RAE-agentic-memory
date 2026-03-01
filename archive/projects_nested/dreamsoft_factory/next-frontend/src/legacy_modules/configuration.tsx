/**
 * Service: configuration
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface ComplexProduct {
    selectedProduct: { data: ProductData };
}

interface ProductData {
    info: {
        name?: string;
        langs: { [key: string]: { name: string } };
        noCalculate?: boolean;
    };
    customFormatInfo: {
        customName: { [key: string]: string };
    };
    currentFormat: {
        name: string;
        customWidth?: string;
        customHeight?: string;
        unit?: number;
    };
    currentPages?: number;
    customPageInfo: {
        customName: { [key: string]: string };
    };
    thickness: {
        current: number;
    };
}

interface Props {
    complexProducts: ComplexProduct[];
    currentLang: { code: string };
    productItem: {
        amount?: number;
        volume?: number;
        realisationTime?: number;
        taxID?: number;
    };
    getTotalThickness: () => number;
}

const ConfigurationPanel: React.FC<Props> = ({ complexProducts, currentLang, productItem, getTotalThickness }) => {
    const tmpProduct = complexProducts.length > 0 ? complexProducts[0].selectedProduct.data : null;

    return (
        <div className="panel panel-info panel-configuration">
            <div className="panel-heading">
                <h3 className="panel-title">
                    {/* Assuming 'translate' is a function that translates the text */}
                    {('configuration_product' as string) | translate}:
                </h3>
            </div>
            <div className="panel-body">
                {complexProducts.map((complexProduct, index) => (
                    <React.Fragment key={index}>
                        {tmpProduct && !tmpProduct.info.noCalculate && (
                            <div>
                                <h4>{tmpProduct.info.langs[currentLang.code] ? tmpProduct.info.langs[currentLang.code].name : tmpProduct.info.name}</h4>
                                <dl className="dl-horizontal">
                                    <dt>
                                        {tmpProduct.customFormatInfo.customName[currentLang.code] 
                                            ? tmpProduct.customFormatInfo.customName[currentLang.code] 
                                            : ('format' as string | (() => JSX.Element)) | translate}
                                    </dt>
                                    <dd>
                                        {tmpProduct.currentFormat.name}
                                        {tmpProduct.currentFormat.custom && (
                                            <div>
                                                {tmpProduct.currentFormat.customWidth} x {tmpProduct.currentFormat.customHeight}{tmpProduct.currentFormat.unit === 2 ? 'cm' : 'mm'}
                                            </div>
                                        )}
                                    </dd>
                                    <dt>{tmpProduct.currentPages > 0 && tmpProduct.customPageInfo.customName[currentLang.code] ? tmpProduct.customPageInfo.customName[currentLang.code] : ('pages' as string | (() => JSX.Element)) | translate}</dt>
                                    <dd>{tmpProduct.currentPages > 0 && tmpProduct.currentPages}</dd>
                                    {tmpProduct.thickness.current !== undefined && (
                                        <div>
                                            <dt>{'thickness' as string | (() => JSX.Element)) | translate}</dt>
                                            <dd>{tmpProduct.thickness.current.toFixed(2)} mm</dd>
                                        </div>
                                    )}
                                </dl>
                            </div>
                        )}
                    </React.Fragment>
                ))}
            </div>
            <div className="panel-footer bg-info">
                {('term_realization_info' as string) | translate}
            </div>
        </div>
    );
};

export default ConfigurationPanel;