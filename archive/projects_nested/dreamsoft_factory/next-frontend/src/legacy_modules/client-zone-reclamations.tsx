/**
 * Service: client-zone-reclamations
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface ReclamationProps {
    reclamation: any;
    currentLang: any;
    formatSizeUnits: (file: any) => string;
    messages: (reclamation: any) => void;
}

const ReclamationComponent: React.FC<ReclamationProps> = ({ reclamation, currentLang, formatSizeUnits, messages }) => {
    return (
        <div>
            <paging on="event"></paging>
            <div ng-if="reclamation.files.admin.length > 0">
                <table className="table table-responsive table-file-list">
                    <caption>{'printing_house_files' | translate}</caption>
                    <tbody>
                        {reclamation.files.admin.map((file: any, index: number) => (
                            <tr key={index}>
                                <td className="image-prev col-md-2">
                                    <img loading="lazy" className="img-responsive" src={file.minUrl} />
                                </td>
                                <td className="file-name">
                                    <a href={file.url} target="_blank" title={'view' | translate}>{file.name}</a>
                                </td>
                                <td className="file-size">{formatSizeUnits(file)}</td>
                                <td className="file-remover"></td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
            <div>
                <b>{'products' | translate}</b>
                <br />
                <ul>
                    {reclamation.products.map((product: any, index: number) => (
                        <li key={index}>
                            {product.type.names[currentLang.code]} (<b>ID: {product.productID}</b>)
                        </li>
                    ))}
                </ul>
            </div>
            <button ng-click="messages(reclamation)" ng-class="{'btn-danger': reclamation.unreadMessages}" className="btn btn-default" type="button">
                {'reclamation_messages' | translate} <i className="fa fa-comments-o" aria-hidden="true"></i>
                {reclamation.unreadMessages && <span className="badge">{reclamation.unreadMessages}</span>}
            </button>
        </div>
    );
};

export default ReclamationComponent;