/**
 * Service: print-offer
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const PrintOffer: React.FC = () => {
    return (
        <div>
            <style jsx>{`
                @page {
                    size: 210mm 297mm;
                    margin: 5mm;
                    margin-header: 5mm;
                    margin-footer: 5mm;
                }

                #content {
                    width: 210mm;
                    margin: 0;
                }

                #content .header {
                    padding: 15px;
                    width: 180mm;
                    border-bottom: 1px solid #e5e5e5;
                }

                #content .header .header-title {
                    font-size: 18px;
                    margin: 0;
                }

                #content .two-columns {
                    display: flex;
                }

                #content .two-columns .column-one {
                    width: 100mm;
                }

                #content .two-columns .column-two {
                    width: 100mm;
                    padding-left: 10mm;
                }

                #content .row .two-columns > tr > td {
                    margin-right: 10mm;
                }

                #content .two-columns tr td .configuration-box {
                    width: 90mm;
                }

                #content .two-columns tr td .configuration-box .panel-header {
                    color: #31708f;
                    background-color: #d9edf7;
                    border-color: #bce8f1;
                    padding: 10px 15px;
                    border-bottom: 1px solid transparent;
                    border-top-right-radius: 3px;
                    border-top-left-radius: 3px;
                }

                #content .two-columns tr td .realizationBox {
                    width: 100mm;
                }

                #content .realizationBox .panel-heading {
                    color: #333333;
                    background-color: #f5f5f5;
                    border-color: #dddddd;
                    padding: 10px 15px;
                    border-bottom: 1px solid transparent;
                    border-top-right-radius: 3px;
                    border-top-left-radius: 3px;
                    border: 1px solid red;
                }
            `}</style>

            <div id="content">
                <div className="header">
                    <h1 className="header-title">{'offer_gen' | translate(lang)}</h1>
                    <span>{offerDate.toISOString()}</span><br />
                    <hr />
                    <span>{type.names[lang]}</span>
                </div>
                <div className="delivery">
                    {('delivery' | translate(lang))}:
                    {selectedDeliveries.map((delivery, index) => (
                        <React.Fragment key={index}>
                            {delivery[lang]}<br />
                        </React.Fragment>
                    ))}
                </div>
                <hr />
                <div className="two-columns">
                    <table>
                        <tbody>
                            <tr>
                                <td className="left-column">
                                    <b>
                                        {complexProduct.format.customNames 
                                            ? complexProduct.format.customNames[lang] 
                                            : ('format' | translate(lang))}
                                    </b>
                                </td>
                                <td className="right-column">
                                    {complexProduct.format.langs && complexProduct.format.langs[lang].name}
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default PrintOffer;