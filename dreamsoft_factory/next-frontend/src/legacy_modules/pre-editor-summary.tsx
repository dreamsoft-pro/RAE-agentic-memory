/**
 * Service: pre-editor-summary
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Props {
    calculation: any;
    currentCurrency: { symbol: string };
    checkPrice: (price: number) => boolean;
    showSumPrice: () => number;
    showSumGrossPrice: () => number;
    net_per_pcs: number;
    gross_per_pcs: number;
    getToken: () => string;
    productItem: { jsonText: string };
}

const SummaryPanel: React.FC<Props> = ({ 
    calculation, 
    currentCurrency, 
    checkPrice, 
    showSumPrice, 
    showSumGrossPrice, 
    net_per_pcs, 
    gross_per_pcs, 
    getToken, 
    productItem 
}) => {
    return (
        <div className="panel panel-default panel-success panel-summary">
            <div className="panel-heading">{'price' | translate}</div>
            <div className="panel-body" style={{display: checkPrice(calculation.priceTotal) ? 'block' : 'none'}}>
                <div className="row">
                    <div className="col-xs-12 col-sm-6">
                        <div className="bg-info summary-price summary-price-net">
                            <b>{'net_price' | translate}:</b>
                            <span className="text-nowrap">
                                <span className="value" style={{display: 'inline'}}>{showSumPrice()}</span>
                                <span className="currency">{currentCurrency.symbol}</span>
                            </span>
                        </div>
                    </div>
                    <div className="col-xs-12 col-sm-6">
                        <div className="bg-info summary-price summary-price-gross">
                            <b>{'gross_price' | translate}:</b>
                            <span className="text-nowrap">
                                <span className="value" style={{display: 'inline'}}>{showSumGrossPrice()}</span>
                                <span className="currency">{currentCurrency.symbol}</span>
                            </span>
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="col-xs-12 col-sm-6">
                        <div className="bg-default price-per-item price-per-item-net">
                            {`${'net' | translate} 1 ${'pcs' | translate}`}:
                            <span className="text-nowrap">{net_per_pcs} {currentCurrency.symbol}</span>
                        </div>
                    </div>
                    <div className="col-xs-12 col-sm-6">
                        <div className="bg-default price-per-item price-per-item-gross">
                            {`${'gross' | translate} 1 ${'pcs' | translate}`}:
                            <span className="text-nowrap">
                                <span className="value">{gross_per_pcs}</span>
                                <span className="currency">{currentCurrency.symbol}</span>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            <div className="panel-body" style={{display: checkPrice(calculation.priceTotal) ? 'none' : 'block'}}>
                <div className="loading text-center text-primary">
                    <i className="fa fa-spinner fa-pulse fa-fw"></i>
                    <span>{'please_wait' | translate}</span>
                </div>
            </div>
            <div className="panel-footer">
                <div className="row">
                    <div className="col-xs-12">
                        <form action="" method="POST" onSubmit={(e) => e.preventDefault()}>
                            <button type="submit" className="btn btn-sm btn-block btn-info">{'go_to_editor' | translate}</button>
                            <input type="hidden" value={getToken()} name="access-token"/>
                            <textarea style={{display: 'none'}} value={productItem.jsonText} name="products"></textarea>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SummaryPanel;