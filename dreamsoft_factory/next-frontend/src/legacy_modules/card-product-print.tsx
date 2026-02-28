/**
 * Service: card-product-print
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface DeliveryAddress {
    delivery: {
        deliveryNames: Record<string, string>;
    };
    address: {
        name: string;
        lastname: string;
        zipcode: string;
        city: string;
        street: string;
        house: string;
        apartment?: string;
    };
    volume: number;
}

interface Attribute {
    emptyChoice: number;
    langs: Record<string, { name: string }>;
    optLangs: Record<string, { name: string }>;
    optName: string;
}

interface SpecialAttribute {
    name: string;
}

interface Props {
    deliveryAddresses: DeliveryAddress[];
    attributes: Attribute[];
    subProduct: {
        specialAttributes: SpecialAttribute[];
    };
    calc: {
        realisationDate: string;
        acceptDate: string;
    };
    types: Record<string, { cardGuide?: boolean }>;
    groups: Record<string, { cardGuide?: boolean }>;
    userData: { name: string };
    logo?: string;
    barCode: string;
    cardID: string;
    countFiles: number;
    coupon?: {
        couponID: string;
        value: number;
        percent?: boolean;
    };
    lang: string;
}

const CardProductPrint: React.FC<Props> = ({ deliveryAddresses, attributes, subProduct, calc, types, groups, userData, logo, barCode, cardID, countFiles, coupon, lang }) => {
    return (
        <div>
            <div className="headerSection">
                <div className="logoSection">
                    {logo && <img loading="lazy" className="logoImage" src={`data:image/jpeg;base64,${logo}`} alt="Logo" />}
                </div>
                <div className="titleSection">
                    <div className="cardTitle">{'product_card' | translate(lang)} - {cardID}</div>
                </div>
                <div className="barCodeSection">
                    <div className="code">{barCode}</div>
                    <div className="cardID">{cardID}</div>
                </div>
            </div>
            {complexProduct && (
                <table className="cardTable">
                    <tr>
                        <th className="mainHeadCell">{'complex_product' | translate(lang)}</th>
                    </tr>
                    <tr>
                        <td className="mainValueCell">{subProduct.names[lang]} - {calc.realisationDate}</td>
                    </tr>
                </table>
            )}
            <br />
            {types[subProduct.typeID].cardGuide || groups[subProduct.groupID].cardGuide ? (
                <table style={{ width: '100%' }}>
                    <tr className="informationRow halfTableRow">
                        <td>
                            <table className="infoTable">
                                <tr>
                                    <th className="keyCell">{'uploaded_files' | translate(lang)}</th>
                                    <td className="valueCell">{countFiles}</td>
                                </tr>
                                {coupon && (
                                    <tr>
                                        <th className="keyProductInfoCell">{'coupon_info' | translate(lang)}</th>
                                        <td className="valueCell">
                                            {coupon.couponID} - {coupon.value}
                                            {coupon.percent ? '%' : calc.currency}
                                        </td>
                                    </tr>
                                )}
                            </table>
                        </td>
                    </tr>
                </table>
            ) : null}
            <br />
            <table className="cardTable" style={{ borderCollapse: 'collapse', marginBottom: 5, verticalAlign: 'middle', width: '100%' }}>
                <tr>
                    <th className="keyCell">{'realization_time' | translate(lang)}</th>
                    <td className="valueCell">{calc.realisationDate}</td>
                </tr>
                <tr>
                    <th className="keyCell">{'accept_date' | translate(lang)}</th>
                    <td className="valueCell">{calc.acceptDate}</td>
                </tr>
            </table>
            {deliveryAddresses.length > 0 && (
                <table style={{ width: '100%' }}>
                    <tr>
                        <th className="deliveryHeadCell">{'delivery_address' | translate(lang)}</th>
                        <th className="deliveryHeadCell">{'volume' | translate(lang)}</th>
                    </tr>
                    {deliveryAddresses.map((deliveryAddress, index) => (
                        <tr key={index}>
                            <td className="deliveryValueCell">{deliveryAddress.delivery.deliveryNames[lang]}</td>
                            <td className="deliveryValueCell">
                                {deliveryAddress.address.name} {deliveryAddress.address.lastname}<br />
                                {deliveryAddress.address.zipcode} {deliveryAddress.address.city}<br />
                                {deliveryAddress.address.street} {deliveryAddress.address.house}
                                {deliveryAddress.address.apartment && `/${deliveryAddress.address.apartment}`}<br /><br />
                            </td>
                            <td className="deliveryValueCell">{deliveryAddress.volume}</td>
                        </tr>
                    ))}
                </table>
            )}
        </div>
    );
};

export default CardProductPrint;