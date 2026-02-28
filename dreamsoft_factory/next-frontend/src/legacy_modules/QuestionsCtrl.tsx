/**
 * Service: QuestionsCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState, useEffect, useRef } from 'react';
import { ApiCollection } from './ApiCollection'; // Assuming you have a similar structure in your project
import _ from 'lodash';

const QuestionsCtrl = () => {
    const [pagingSettings, setPagingSettings] = useState({ pageSize: 0 });
    const [pageSizeSelect, setPageSizeSelect] = useState([]);
    const [offerFilters, setOfferFilters] = useState({ dateFrom: null, dateTo: null, text: null });
    const [customProductsCtrl, setCustomProductsCtrl] = useState(null);
    const [timerId, setTimerId] = useState(null);

    useEffect(() => {
        const customProductConfig = {
            count: 'dp_customProducts/publicCount',
            params: { limit: pagingSettings.pageSize },
            onSuccess: (data) => {
                // Assuming you have a similar structure for items and isCollapsed
                setCustomProductsCtrl({
                    items: data.map(offer => ({ ...offer, isCollapsed: true, contentArray: offer.content.split('\n') })),
                    count: data.count
                });
            }
        };

        const ctrl = new ApiCollection('dp_customProducts/getPublic', customProductConfig);
        setCustomProductsCtrl(ctrl);
        ctrl.get();
    }, [pagingSettings.pageSize]);

    useEffect(() => {
        if (offerFilters.dateFrom && offerFilters.dateTo) {
            const dateFrom = Math.floor(offerFilters.dateFrom.getTime() / 1000);
            const dateTo = Math.floor((offerFilters.dateTo.getTime() / 1000) + (60 * 60 * 24));
            customProductsCtrl?.setParams({ dateFrom, dateTo });
        }
    }, [offerFilters]);

    return (
        <div>
            {/* Your JSX elements here */}
        </div>
    );
};

export default QuestionsCtrl;