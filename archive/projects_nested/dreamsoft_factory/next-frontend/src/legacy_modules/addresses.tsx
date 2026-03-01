/**
 * Service: addresses
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useTranslation } from 'react-i18next';

const Addresses: React.FC = () => {
    const { t } = useTranslation();
    const [addresses, setAddresses] = React.useState([]);
    const [form, setForm] = React.useState({
        addressName: '',
        name: '',
        // other form fields...
    });

    return (
        <div className="modal-header">
            <h4 className="modal-title">{t('addresses')}</h4>
        </div>
        <div className="modal-body">
            {/* Lista adresów do produktów */}
            {addresses.map((address, index) => (
                <div key={index} className="row">
                    <div className="col-md-4">
                        <b>{t('sender_address')}</b>
                        <br />
                        {address.senderID === 2 ? (
                            <>
                                {address.sender.companyID.length > 0 && <div>{address.sender.company}<br /></div>}
                                {address.sender.name} {address.sender.lastname}<br />
                                {address.sender.zipcode} {address.sender.city}<br />
                                {address.sender.street} {address.sender.house} 
                                <span>
                                    {address.sender.apartment.length > 0 && `/${address.sender.apartment}`}
                                </span><br />
                                <b>{t('phone')}</b> +{address.sender.areaCode} {address.sender.telephone}<br />
                            </>
                        ) : (
                            <>{t('sender_printhouse')}</>
                        )}
                    </div>
                </div>
            ))}

            <div className="row voffset5">
                <div className="col-md-6 requiredFields">
                    <span>* - {t('fields_with_star_required')}</span>
                </div>
            </div>
        </div>
    );
};

export default Addresses;