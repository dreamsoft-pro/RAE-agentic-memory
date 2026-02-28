/**
 * Service: product-files-common
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface File {
    minUrl: string;
    name: string;
    url: string;
    size: number;
    type: string;
    widthNet?: number;
    heightNet?: number;
    acceptChangeDate?: string;
    // Add other necessary file properties here
}

interface Product {
    availableFilesToFix: boolean;
    sendToFix: boolean;
    volume: number;
    calcProducts: any[]; // Adjust the type as per your actual data structure
    fileList: {
        files: File[];
        typeLangs: any;
        langs: any;
        optLangs: any;
    }[];
}

interface Props {
    product: Product;
    fixFile: boolean;
    currentLang: { code: string };
    formatSizeUnits: (size: number) => string;
    isAllowDivideText: (product: Product, filesVolume: number) => boolean;
    saveProductProps: (product: Product) => void;
    updateVolumeNumber: (product: Product) => void;
    checkMultivolume: (file: File, product: Product) => void;
}

const ProductFilesComponent: React.FC<Props> = ({ product, fixFile, currentLang, formatSizeUnits, isAllowDivideText, saveProductProps, updateVolumeNumber, checkMultivolume }) => {
    return (
        <table className="table table-file-list wt-responsive-table">
            <caption>
                {/* Translate function not defined here */}
                Files
                {product.availableFilesToFix && product.sendToFix !== undefined && (
                    <label style={{ float: 'right' }}>
                        <input 
                            type="checkbox" 
                            checked={product.sendToFix} 
                            onChange={(e) => saveProductProps({ ...product, sendToFix: e.target.checked })}
                        />
                        {/* Translate function not defined here */}
                        Send files to fix
                    </label>
                )}
            </caption>
            <thead>
                <tr>
                    <th></th>
                    <th>{/* Translate function not defined here */}Preview</th>
                    <th>{/* Translate function not defined here */}Name</th>
                    <th>{product.allowVolumeDivide && isMoreFiles(product) ? /* Translate function not defined here */ 'Volume' : null}</th>
                    <th>{/* Translate function not defined here */}Details</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {product.fileList.map((attrData, index) => (
                    <React.Fragment key={index}>
                        {attrData.files.map((file: File, fileIndex) => (
                            <tr key={fileIndex}>
                                <td>
                                    {/* Add logic for multiple types if necessary */}
                                    <span>{file.name}</span>
                                    {isSideAssign(attrData, file, product) && (
                                        <select 
                                            value={file.backSideTarget} 
                                            onChange={(e) => selectFileTarget(product, file)}
                                        >
                                            <option value="0">{/* Translate function not defined here */}Front side</option>
                                            <option value="1">{/* Translate function not defined here */}Back side</option>
                                        </select>
                                    )}
                                </td>
                                <td className="image-prev">
                                    <img src={file.minUrl} alt="" className="img-responsive" loading="lazy" />
                                </td>
                                <td className="file-name">
                                    {file.url && (
                                        <a href={file.url} target="_blank" title="View">{file.name}</a>
                                    )}
                                </td>
                                <td>
                                    {product.allowVolumeDivide && attrData.files.length > 1 && (
                                        <input 
                                            type="number" 
                                            min="1" 
                                            placeholder={/* Translate function not defined here */ 'volume_to_divide_placeholder'}
                                            value={file.volume}
                                            onChange={(e) => checkMultivolume(file, product)}
                                        />
                                    )}
                                </td>
                                <td className="file-size">
                                    {file.minUrl && formatSizeUnits(file.size)}
                                    {file.type === 'pdf' && !dimensionsValid(file, product, 'net') && (
                                        <span>{/* Translate function not defined here */}Net dimensions: {product.calcProducts[0].formatWidth - 2 * product.calcProducts[0].slope}x{product.calcProducts[0].formatHeight - 2 * product.calcProducts[0].slope}</span>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </React.Fragment>
                ))}
            </tbody>
        </table>
    );
};

export default ProductFilesComponent;