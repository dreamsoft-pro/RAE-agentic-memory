/**
 * Service: products-list-mail
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Product {
    productID: string;
    calcID: number;
    ver: number;
    names: { [key: string]: string };
    isMultiVolumeOffer: number;
    currentMultiOfferVolumes: number[];
    name: string;
    calcProducts: CalcProduct[];
}

interface CalcProduct {
    typeLangs: { [key: string]: { name: string } };
    customFormatName: { [key: string]: string };
    formatLangs: { [key: string]: { name: string } };
    formatName: string;
}

interface Props {
    products: Product[];
    lang: string;
}

const ProductsListMail: React.FC<Props> = ({ products, lang }) => {
    return (
        <center>
            <table width="100%" style={{ borderCollapse: 'collapse', borderSpacing: 0, height: '100%', margin: 0, padding: 0 }}>
                <thead>
                    <tr style={{ borderBottom: '10px solid #e3e3e3', backgroundColor: '#e3e3e3', color: '#333' }}>
                        <th width="55%" style={{ padding: '8px 0' }}>{'name'.toUpperCase()}</th>
                        <th width="15%" style={{ padding: '8px 0' }}>{'quantity'.toUpperCase()}</th>
                        <th width="15%" style={{ padding: '8px 0' }}>{'net_price'.toUpperCase()}</th>
                        <th width="15%" style={{ padding: '8px 0' }}>{'gross_price'.toUpperCase()}</th>
                    </tr>
                </thead>
                <tbody>
                    {products.map((product, index) => (
                        <tr key={product.productID} style={{ marginBottom: 10, borderBottom: '1px solid #e5e5e5', borderRight: '1px solid #e5e5e5', borderLeft: '1px solid #e5e5e5', backgroundColor: index % 2 === 0 ? '#e5e5e5' : '' }}>
                            <td style={{ padding: '10px 10px 10px 20px', borderRight: product.isMultiVolumeOffer ? 'none' : '1px solid #e5e5e5', backgroundColor: index % 2 === 0 ? '#fff' : '' }}>
                                <b>{'product_id'.toUpperCase()}: {product.productID}</b><br />
                                {'calculation_no'.toUpperCase()}: {product.calcID}/{product.ver}<br /><br />
                                {product.calcProducts.length > 1 && (
                                    <b>{product.names[lang]}</b><br /><br>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </center>
    );
};

export default ProductsListMail;