/**
 * Service: CurrencyCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from './store/rootReducer';
import { switchCurrency as switchCurrencyAction } from './actions/currencyActions';
import UserService from './services/UserService';

const CurrencyCtrl: React.FC = () => {
    const dispatch = useDispatch();
    const [currentCurrency, setCurrentCurrency] = useState<any>(null);
    const rootState = useSelector((state: RootState) => state);

    useEffect(() => {
        if (rootState.logged && rootState.user && rootState.user.userID) {
            UserService.editUserOptions(rootState.user.userID, { currency: currentCurrency }).then((savedData) => {
                console.log(savedData);
            });
        }
    }, [currentCurrency, rootState.logged, rootState.user, rootState.user.userID]);

    const handleSwitchCurrency = (currency: any) => {
        if (rootState.currentCurrency === currency) {
            return;
        }

        setCurrentCurrency(currency);
        dispatch(switchCurrencyAction(currency));
    };

    return null; // React functional component should always return a JSX element or null
};

export default CurrencyCtrl;
