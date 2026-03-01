/**
 * Service: summary
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

const SummaryPanel = ({ currentCurrency, net_per_pcs, gross_per_pcs, showSumPrice, showSumGrossPrice, getToken, productItem, printOffer, toCart, deliveryLackOfVolume, currentType, currentCalc }) => {
    const { t } = useTranslation();

    return (
        <div className="panel panel-default panel-success panel-summary">
            <div className="panel-heading">{t('summary')}</div>
            <div className="panel-body">
                <div className="row">
                    <div className="col-xs-12 col-sm-6">
                        <div className="bg-info summary-price summary-price-net">
                            <b>{t('net_price')}:</b>
                            <span className="text-nowrap">
                                <span className="value">{showSumPrice()}</span>
                                <span className="currency">{currentCurrency.symbol}</span>
                            </span>
                        </div>
                    </div>
                    <div className="col-xs-12 col-sm-6">
                        <div className="bg-info summary-price summary-price-gross">
                            <b>{t('gross_price')}:</b>
                            <span className="text-nowrap">
                                <span className="value">{showSumGrossPrice()}</span>
                                <span className="currency">{currentCurrency.symbol}</span>
                            </span>
                        </div>
                    </div>
                </div>
                <div className="row">
                    <div className="col-xs-12 col-sm-6">
                        <div className="bg-default price-per-item price-per-item-net">
                            {t('net')} 1 {t('pcs')}:
                            <span className="text-nowrap">{net_per_pcs} {currentCurrency.symbol}</span>
                        </div>
                    </div>
                    <div className="col-xs-12 col-sm-6">
                        <div className="bg-default price-per-item price-per-item-gross">
                            {t('gross')} 1 {t('pcs')}:
                            <span className="text-nowrap">
                                <span className="value">{gross_per_pcs}</span>
                                <span className="currency">{currentCurrency.symbol}</span>
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            <div className="panel-footer">
                <div className="row">
                    <div className="col-xs-12">
                        {currentType.isEditor === 1 && !currentCalc ? (
                            <form action="" method="POST" onSubmit={(e) => e.preventDefault()}>
                                <button type="submit" className="btn btn-sm btn-block btn-info">{t('go_to_editor')}</button>
                                <input type="hidden" value={getToken()} name="access-token" />
                                <textarea style={{ display: 'none' }} value={productItem.jsonText} name="products"></textarea>
                            </form>
                        ) : null}
                        {!currentCalc ? (
                            <a onClick={printOffer} className="btn btn-block btn-info">{t('print_offer')}</a>
                        ) : null}
                        {!currentCalc && deliveryLackOfVolume > 0 ? (
                            <a disabled={deliveryLackOfVolume > 0} onClick={toCart} className="btn btn-success btn-block btn-lg">{t('add_to_cart')}</a>
                        ) : null}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SummaryPanel;