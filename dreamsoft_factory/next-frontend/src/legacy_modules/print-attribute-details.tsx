/**
 * Service: print-attribute-details
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

const PrintAttributeDetails: React.FC = () => {
    return (
        <div>
            <style jsx>{`
                @page {
                    size: 210mm 297mm;
                    margin: 5mm;
                    margin-header: 5mm;
                    margin-footer: 5mm;
                    font-family: Helvetica;
                }

                #content {
                    width: 210mm;
                    /* background: #d6d6d6; */
                    margin: 0;
                }

                .paperImage {
                    width: 100%;
                    height: auto;
                }

                .logoImage {
                    width: 55mm;
                    height: auto;
                }

                .descriptionTable {
                    width: 100%;
                }

                .descriptionTable td {
                    vertical-align: top;
                }

                .descriptionTable .imageCol {
                    width: 20%;
                }

                .descriptionTable .descriptionCol {
                    width: 80%;
                    padding-left: 30px;
                }

                .singleDesc span {
                    color: #e6b382;
                }

                .lineBreak {
                    width: 100%;
                    height: 1px;
                    margin: 10mm 0 5mm;
                    background: black;
                }

                .attrsTable {
                    width: 100%;
                }

                .attrsTable tr {
                    width: 100%;
                }

                .attrsTable td {
                    vertical-align: top;
                }

                .attrsTable .nameCol {
                    width: 20%;
                }

                .attrsTable .dataCol {
                    width: 25%;
                    padding-left: 1%;
                }

                .attrsTable .productsCol {
                    width: 50%;
                    padding-left: 1%;
                    padding-top: 5mm;
                }

                .singleDescGroup {
                    padding-left: 10px;
                }
            `}</style>

            <body>
                <div id="content">
                    <div className="modal-body">
                        <table className="attrsTable">
                            <tr>
                                <td className="nameCol">
                                    <b>{'description' | translate(lang)}</b>
                                </td>
                                <td className="dataCol">
                                    <div className="singleDesc">
                                        <span>{'whiteness' | translate(lang)}:</span> {whiteness}
                                    </div>
                                    <div className="singleDesc">
                                        <span>{'sizePage' | translate(lang)}:</span> {sizePage}
                                    </div>
                                    <div className="singleDesc">
                                        <span>{'opacity' | translate(lang)}:</span> {opacity}
                                    </div>
                                    <div className="singleDesc">
                                        <span>{'colorOfThePaper' | translate(lang)}:</span> {colorOfThePaper}
                                    </div>
                                    <div className="singleDesc">
                                        <span>{'smoothnessRoughness' | translate(lang)}:</span> {smoothnessRoughness}
                                    </div>
                                </td>
                                <td className="productsCol">
                                    {products.map((product, index) => (
                                        <React.Fragment key={index}>
                                            {product[lang]}<br />
                                        </React.Fragment>
                                    ))}
                                </td>
                            </tr>
                        </table>
                        {altPapers && (
                            <div className="lineBreak"></div>
                        )}
                        {altPapers && (
                            <table className="attrsTable">
                                <tr>
                                    <td className="nameCol">
                                        <b>{'alternative_papers' | translate(lang)}</b>
                                    </td>
                                    <td className="productsCol">
                                        {altPapers.map((altPaper, index) => (
                                            <React.Fragment key={index}>
                                                {altPaper.name}<br />
                                            </React.Fragment>
                                        ))}
                                    </td>
                                </tr>
                            </table>
                        )}
                    </div>
                </div>
                <img loading="lazy" className="logoImage" src="https://buchdruckerei.de/wp-content/themes/twentytwenty/assets/images/logo.png" />
                <h3 className="pageTitle">{paper_type}</h3>
                <table className="descriptionTable">
                    <tr>
                        <td className="imageCol">
                            {imageUrl ? (
                                <img loading="lazy" className="paperImage" src={imageUrl} />
                            ) : (
                                <img loading="lazy" className="paperImage" src="https://buchdruckerei.de/wp-content/themes/twentytwenty/assets/images/paper_cover.png" />
                            )}
                        </td>
                    </tr>
                </table>
            </body>
        </div>
    );
};

export default PrintAttributeDetails;