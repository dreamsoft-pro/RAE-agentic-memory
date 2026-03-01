/**
 * Service: client-zone-orders
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface Order {
    waitForAccept: number;
    filesAlert: number;
    filesRejected: number;
    reportsToAccept: number;
    acceptCanceled: boolean;
}

interface Product {
    deliveryPrice: number;
    deliveryJoined: number;
    name: string;
    productID: string;
}

interface File {
    id: string;
    name: string;
    accept: number;
    acceptChangeDate: string;
    created: string;
    comment: string;
}

interface Props {
    order: Order;
    product: Product;
    files: File[];
    translate: (key: string) => string;
}

const ClientZoneOrders: React.FC<Props> = ({ order, product, files, translate }) => {
    const getFileAlertClass = (file: File): string => {
        if (order.filesRejected > 0) return 'text-reject-black file-alert pull-right';
        if (order.waitForAccept > 0 && order.filesAlert == 0 && order.filesRejected == 0) return 'text-info file-alert pull-right';
        return '';
    };

    return (
        <div>
            {/* File Alerts */}
            <span className={getFileAlertClass(file)}>
                {order.filesRejected > 0 ? translate('files_rejected') : (
                    order.waitForAccept > 0 && order.filesAlert == 0 && order.filesRejected == 0 ? translate('files_waiting_to_be_approved') : ''
                )}
                <i className="fa fa-file"></i>
            </span>

            {/* Delivery Address */}
            <div className="row">
                <div className="col-md-2">
                    <b>{translate('name')}</b>
                    <br />
                    {product.name}
                </div>
                <div className="col-md-2">
                    <b>{translate('product_number')}</b>
                    <br />
                    {product.productID}
                </div>
            </div>

            {/* Files Table */}
            <div>
                <table>
                    <tbody>
                        {files.map(file => (
                            <tr key={file.id}>
                                <td>{file.name}</td>
                                <td className="file-accept">
                                    <span ng-if="file.accept == 1">{translate('file_accepted')}</span>
                                    <span ng-if="file.accept == -1">{translate('file_rejected')}</span>
                                    {file.accept != 0 && (
                                        <div>{translate('date')} {file.acceptChangeDate}</div>
                                    )}
                                    {file.accept == 0 && (
                                        <div>{translate('add_date')} {file.created}</div>
                                    )}
                                </td>
                                <td>{file.comment}</td>
                                <td className="file-remover">
                                    {file.accept == 0 && (
                                        <button ng-click="acceptReport(product, file)" className="btn btn-xs btn-success">{translate('accept')}</button>
                                    )}
                                    {file.accept == 0 && (
                                        <button ng-click="rejectReport(product, file)" type="button" className="btn btn-xs btn-danger">{translate('reject')}</button>
                                    )}
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default ClientZoneOrders;