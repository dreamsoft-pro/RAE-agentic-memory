/**
 * Service: _printoffer
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const PrintOffer = ({ offerdata, companyID, currentCurrency, deliveries, group, loadVolumes, po_logo, rtVolumes, showSumGrossPrice, showSumPrice, staticContent }) => {
    const STATIC_URL = "yourStaticUrl"; // Replace with actual static URL
    const currentLang = { code: 'en' }; // Assuming a default language
    const offerdate = new Date(); // Assuming the date is fetched or set here

    return (
        <div id="content">
            <div className="modal-header">
                <h4>{'offer_for_print' | translate}</h4>
            </div>
            <div className="modal-body">
                <div className="row">
                    <div className="col-sm-6">
                        <img loading="lazy" src={`${STATIC_URL}uploadedFiles/${companyID}/logo`} alt="Logo" className="img-responsive" />
                        <hr />
                        <dl className="dl-horizontal">
                            {offerdata.name && (
                                <>
                                    <dt>{'order_name' | translate}</dt>
                                    <dd>{offerdata.name}</dd>
                                </>
                            )}
                            <dt>{'offer_gen' | translate}</dt>
                            <dd>{offerdate.toISOString().replace('T', ' ').substring(0, 19)}</dd>
                            <dt>{group.names[currentLang.code]}</dt>
                            <dd>{`${offerdata.cps[0].data.currentFormat.name}, ${offerdata.products[0].pages} pages, ${offerdata.volume} pieces`}</dd>
                        </dl>
                        <table className="table">
                            <caption>{'delivery' | translate}:</caption>
                            {offerdata.productAddresses.map(address => deliveries.filter(delivery => delivery.ID === address.deliveryID).map(delivery => (
                                <span key={delivery.ID}>{delivery.names[currentLang.code]}<br /></span>
                            )))}
                            <tr>
                                <th>{'net_price_with_delivery' | translate}</th>
                                <th>{'gross_price_with_delivery' | translate}</th>
                            </tr>
                            <tr>
                                <td><span>{showSumPrice()}</span> {currentCurrency.symbol}</td>
                                <td><span>{showSumGrossPrice()}</span> {currentCurrency.symbol}</td>
                            </tr>
                        </table>
                    </div>
                    <div className="col-sm-6">
                        {po_logo && (
                            <img loading="lazy" src={po_logo} alt="PO Logo" className="img-responsive" />
                        )}
                    </div>
                </div>
                <hr />
                <div className="row">
                    <div className="col-sm-6 col-sm-12">
                        {/* Assuming configuration.html content is dynamically included here */}
                    </div>
                    <div className="col-sm-6">
                        <div className="panel panel-default">
                            <div className="panel-heading">{'volume_of_product_and_date_of_realization' | translate}</div>
                            {loadVolumes ? (
                                <div className="loading text-center text-primary">
                                    <i className="fa fa-spinner fa-pulse fa-fw"></i>
                                    <span>{'please_wait' | translate}</span>
                                </div>
                            ) : (
                                <table className="table table-bordered">
                                    <thead>
                                        <th>{'volume' | translate}</th>
                                        <th>
                                            {'price' | translate}/{'volume' | translate}
                                            <br />
                                            {'net_price' | translate}/{'gross_price' | translate}
                                        </th>
                                        <th>
                                            {'price' | translate}/{'unit' | translate}
                                            <br />
                                            {'net_price' | translate}/{'gross_price' | translate}
                                        </th>
                                    </thead>
                                    <tbody>
                                        {rtVolumes.map(volume => (
                                            <tr key={volume.qty} className={(volume.qty === calculation.volume) ? 'bg-success' : ''}>
                                                <td>{volume.qty}</td>
                                                <td><b>{volume.net | priceFilter} {currentCurrency.symbol}</b><br /><small>{volume.gross | priceFilter} {currentCurrency.symbol}</small></td>
                                                <td><b>{volume.netunit | priceFilter} {currentCurrency.symbol}</b><br /><small>{volume.grossunit | priceFilter} {currentCurrency.symbol}</small></td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                            )}
                        </div>
                    </div>
                </div>
                <hr />
                <div className="row">
                    <div className="col-sm-12">
                        <div data-ng-static-contents dangerouslySetInnerHTML={{__html: staticContent.print_offer}}></div>
                    </div>
                </div>
            </div>
            <div className="modal-footer">
                <button className="btn red-sunglo" onClick={() => { /* cancel action */ }}>{'cancel' | translate}</button>
                <button className="btn btn-success" onClick={() => { /* print action */ }}><i className="fa fa-print"></i> {'text_print' | translate}</button>
            </div>
        </div>
    );
};

export default PrintOffer;