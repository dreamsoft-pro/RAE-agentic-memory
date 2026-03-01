/**
 * Service: OffersCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState, useEffect } from 'react';
import _ from 'lodash';
import { $timeout } from './services/timeoutService'; // Assuming you have a timeout service
import { Notification } from './services/notificationService'; // Assuming you have a notification service
import { $filter } from './services/filterService'; // Assuming you have a filter service
import { ClientZoneWidgetService } from './services/clientZoneWidgetService';
import { AddressService } from './services/addressService';
import { DeliveryService } from './services/deliveryService';
import { Notification } from 'react-notification-system-react'; // Assuming you have a notification service

const OffersCtrl: React.FC = () => {
    const [offers, setOffers] = useState([]);
    const [pagingSettings, setPagingSettings] = useState({ total: 0 });
    const [offerFilters, setOfferFilters] = useState({ dateFrom: '', dateTo: '' });

    useEffect(() => {
        getOffers(1).then((offers) => {
            setOffers(offers);
        }).catch((error) => {
            console.error('fetch error', error);
        });
    }, []);

    const getOffers = async (page: number) => {
        try {
            const response = await ClientZoneWidgetService.countOrders({ 'isOffer': 1 });
            return response.data;
        } catch (error) {
            console.error('fetch error', error);
            throw error;
        }
    };

    const getFlagClass = (addresses: any[], addressID: string) => {
        const selectedAddress = _.find(addresses, { ID: addressID });
        return selectedAddress ? `flag-icon-${selectedAddress.countryCode.toLowerCase()}` : '';
    };

    const search = () => {
        let timeout: any = null;
        timeout = $timeout(() => {
            getNextPage(1);
            timeout = null;
        }, 500);
    };

    const getNextPage = async (page: number) => {
        try {
            const offers = await getOffersWithAdditionalData(page);
            setOffers(offers);
        } catch (error) {
            console.error('Error fetching next page', error);
        }
    };

    const countOffers = async () => {
        try {
            const count = await ClientZoneWidgetService.countOrders({ 'isOffer': 1 });
            setPagingSettings({ total: count.data.count });
            return count.data.count;
        } catch (error) {
            console.error('Error counting offers', error);
            throw error;
        }
    };

    const handleFilterOffers = () => {
        init();
    };

    const handleFilterOffersDate = () => {
        if (offerFilters.dateFrom && offerFilters.dateTo) {
            init();
        }
    };

    const init = () => {
        // Initialization logic here
    };

    return (
        <div>
            {/* Render your component UI here */}
        </div>
    );
};

export default OffersCtrl;