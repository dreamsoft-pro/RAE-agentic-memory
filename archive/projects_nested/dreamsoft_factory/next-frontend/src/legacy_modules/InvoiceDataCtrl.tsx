/**
 * Service: InvoiceDataCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { getDefaultAddress, editUserAddress } from './actions/addressActions';
import { Notification } from './services/NotificationService';
import { translateFilter } from './filters/translateFilter';
import { DpAddressService } from './services/DpAddressService';
import { CountriesService } from './services/CountriesService';

const InvoiceDataCtrl: React.FC = () => {
    const [form, setForm] = useState({ type: 0, default: 0, ID: '' });
    const [countries, setCountries] = useState([]);
    const dispatch = useDispatch();

    useEffect(() => {
        init();
    }, []);

    const init = () => {
        getDefaultAddress();
    };

    const getDefaultAddress = async () => {
        try {
            const data = await DpAddressService.getDefaultAddress(2);
            setForm(data.address);
            const dataCountries = await CountriesService.getAll();
            setCountries(dataCountries);
        } catch (error) {
            console.error('Error fetching default address:', error);
        }
    };

    const editAddress = async () => {
        form.type = 2;
        form.default = 1;

        try {
            const data = await DpAddressService.editUserAddress(form, form.ID);
            if (data.response === true) {
                Notification.success(translateFilter('successfully_edited'));
            } else {
                Notification.error(translateFilter('error'));
            }
        } catch (error) {
            Notification.error(translateFilter('error'));
        }
    };

    return (
        <div>
            {/* React component logic here */}
        </div>
    );
};

export default InvoiceDataCtrl;
