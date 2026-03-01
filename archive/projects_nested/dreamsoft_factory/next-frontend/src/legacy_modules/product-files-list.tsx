/**
 * Service: product-files-list
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Product {
    orderNumber: string;
    ID: string;
    names: { [key: string]: string };
    volume: string;
}

interface File {
    name: string;
    url: string;
    minUrl: string;
    accept: number;
    created: Date;
}

interface Props {
    product: Product;
    files: File[];
    lang: string;
    translate: (key: string, lang?: string) => string;
}

const ProductFilesList: React.FC<Props> = ({ product, files, lang, translate }) => {
    return (
        <center>
            <h2>{translate('product', lang)}</h2>
            <table width="100%" style={{ borderCollapse: 'collapse', borderSpacing: 0, margin: '0px', padding: '0px', color: '#333', border: '1px solid #b0b1b4' }}>
                <thead>
                    <tr style={{ borderBottom: '10px solid', background: '#e8eaf1', textAlign: 'left', margin: '0px 5px' }}>
                        <th width="15%" style={{ textAlign: 'center', padding: '8px 0px', borderRight: '1px solid #b0b1b4' }}>{translate('order_id', lang)}</th>
                        <th width="15%" style={{ textAlign: 'center', padding: '8px 0px', borderRight: '1px solid #b0b1b4' }}>{translate('product_id', lang)}</th>
                        <th width="45%" style={{ textAlign: 'center', padding: '8px 0px', borderRight: '1px solid #b0b1b4' }}>{translate('name', lang)}</th>
                        <th width="15%" style={{ textAlign: 'center', padding: '8px 0px' }}>{translate('volume', lang)}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style={{ textAlign: 'center', padding: '8px 0px', borderRight: '1px solid #b0b1b4' }}>{product.orderNumber}</td>
                        <td style={{ textAlign: 'center', padding: '8px 0px', borderRight: '1px solid #b0b1b4' }}>{product.ID}</td>
                        <td style={{ textAlign: 'center', padding: '8px 0px', borderRight: '1px solid #b0b1b4' }}>{product.names[lang]}</td>
                        <td style={{ textAlign: 'center', padding: '8px 0px' }}>{product.volume}</td>
                    </tr>
                </tbody>
            </table>
            <h2>{translate('files', lang)}</h2>
            <table width="100%" style={{ borderCollapse: 'collapse', borderSpacing: 0, margin: '0px', padding: '0px', color: '#333', border: '1px solid #b0b1b4' }}>
                <thead>
                    <tr style={{ borderBottom: '10px solid', background: '#e8eaf1', textAlign: 'left', margin: '0px 5px' }}>
                        <th width="30%" style={{ textAlign: 'center', padding: '8px 0px', borderRight: '1px solid #b0b1b4' }}>{translate('file_name', lang)}</th>
                        <th width="40%" style={{ textAlign: 'center', padding: '8px 0px', borderRight: '1px solid #b0b1b4' }}>{translate('file', lang)}</th>
                        <th width="15%" style={{ textAlign: 'center', padding: '8px 0px', borderRight: '1px solid #b0b1b4' }}>{translate('date', lang)}</th>
                        <th width="15%" style={{ textAlign: 'center', padding: '8px 0px' }}>{translate('accepted', lang)}</th>
                    </tr>
                </thead>
                <tbody>
                    {files.map((file, index) => (
                        <tr key={index} style={{ background: file.accept === -1 ? '#ff804f' : file.accept === 1 ? '#83e871' : 'white' }}>
                            <td style={{ padding: '8px', borderRight: '1px solid #b0b1b4' }}>{file.name}</td>
                            <td>
                                <a href={file.url} target="_blank">
                                    <img loading="lazy" src={file.minUrl} alt={file.name} style={{ maxWidth: '400px', maxHeight: '100px', padding: '5px' }} />
                                </a>
                            </td>
                            <td style={{ textAlign: 'center' }}>{file.accept === 1 ? translate('yes', lang) : translate('no', lang)}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </center>
    );
};

export default ProductFilesList;