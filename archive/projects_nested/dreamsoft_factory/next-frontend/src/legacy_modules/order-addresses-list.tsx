/**
 * Service: order-addresses-list
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';

interface AddressItem {
    addressName: string;
    street: string;
    zipcode: string;
    city: string;
    edit: {
        areaCode: string;
        telephone: string;
        street: string;
        house: string;
    };
    default: number;
}

interface Props {
    addresses: AddressItem[];
    logged: boolean;
    userCanEdit: boolean;
    form: any; // Assuming this is a form object, adjust the type as necessary
    editAddress: (item: AddressItem) => void;
}

const OrderAddressesList: React.FC<Props> = ({ addresses, logged, userCanEdit, form, editAddress }) => {
    return (
        <div>
            <div className="modal-header">
                <h4 className="modal-title">{'addresses' | translate}</h4>
            </div>
            <div className="modal-body">
                {logged ? (
                    <div className="row">
                        <div className="col-md-12">
                            <div className="list-group">
                                {addresses.map((item, index) => (
                                    <div key={index} className="list-group-item">
                                        <i className="fa fa-book"></i>
                                        <span className="bold">{item.addressName}</span>, 
                                        <span className="bold">{item.street}</span>, 
                                        <span className="bold">{item.zipcode} {item.city}</span> | 
                                        <a href="#" onClick={() => editAddress(item)}>{'edit' | translate}</a>
                                        {item.default === 1 && (
                                            <span className="defaultAddress">
                                                <small> ({'default' | translate})</small>
                                            </span>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                ) : (
                    <div className="row" ng-if="!logged">
                        <div className="col-md-12">{'only_for_users' | translate}</div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default OrderAddressesList;