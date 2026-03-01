/**
 * Service: CartVerifyCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

Here is the modernized version of your JavaScript file (`CartVerifyCtrl.js`) converted to TypeScript and using React functional components with hooks such as `useEffect` and `useState`. This conversion assumes you are familiar with TypeScript and basic React concepts, focusing on type safety and cleaner syntax.

import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { useHistory, useLocation, useParams } from 'react-router-dom';
import { Notification } from '@dp/client-notification'; // Assuming this is a module you are using for notifications
import _ from 'lodash';
import { DpOrderService, ClientZoneWidgetService, UserService, AuthService, TokenService } from './services';
import { RootState } from './store'; // Adjust the import according to your Redux structure

const CartVerifyCtrl: React.FC = () => {
    const [isOnline, setIsOnline] = useState(false);
    const [transactionConfirm, setTransactionConfirm] = useState(false);
    const [wasOneTimeUser, setWasOneTimeUser] = useState(false);
    const [products, setProducts] = useState<any[]>([]);
    const [order, setOrder] = useState<{ [key: string]: any }>({});

    const dispatch = useDispatch();
    const history = useHistory();
    const location = useLocation();
    const { orderid } = useParams<{ orderid?: string }>();
    const rootState = useSelector((state: RootState) => state);

    useEffect(() => {
        const init = async () => {
            let orderID = (location.search as any).orderID || orderid;
            if (!orderID) return;

            let urlParams: { [key: string]: any } = {};

            if (orderID === 'tinkoff') {
                urlParams = {
                    OrderId: (location.search as any).OrderId,
                    PaymentId: (location.search as any).PaymentID
                };
            } else if ((location.search as any).provider === 'paypal') {
                urlParams = {
                    token: (location.search as any).token,
                    PayerID: (location.search as any).PayerID
                };
            } else if ((location.search as any).orderId !== undefined) {
                urlParams.orderId = (location.search as any).orderId;
            }

            try {
                const statusResponse = await DpOrderService.sendPaymentStatus(orderID, urlParams);
                setProducts(statusResponse.products);
                if (statusResponse.orderInfo) {
                    setOrder({
                        finalPrice: statusResponse.orderInfo.finalPrice,
                        currency: statusResponse.orderInfo.currency,
                        orderNumber: statusResponse.orderInfo.orderID,
                        ID: statusResponse.orderInfo.orderID
                    });
                } else {
                    Notification.error('unexpected_error');
                }
            } catch (error) {
                Notification.error('unexpected_error');
            }
        };

        init();
    }, [location, orderid]);

    useEffect(() => {
        if (rootState.statusResponse?.paymentOnline === true) {
            setIsOnline(true);
        }
        if (rootState.statusResponse?.paymentStatus === true) {
            setTransactionConfirm(true);
        }
    }, [rootState.statusResponse]);

    useEffect(() => {
        const fetchPayments = async () => {
            const paymentsData = await ClientZoneWidgetService.getPayments();
            if (rootState.statusResponse?.order && rootState.payments) {
                const selectedPayment = _.find(rootState.payments, { ID: rootState.statusResponse.order.paymentID });
                setProducts(selectedPayment);
            }
        };

        fetchPayments();
    }, [rootState.payments]);

    useEffect(() => {
        const checkOneTimeUser = async () => {
            const data = await UserService.checkOneTimeUser();
            if (data.response === true) {
                try {
                    await AuthService.logout();
                    const nonUserToken = await TokenService.getNonUserToken();
                    dispatch({ type: 'SET_LOGGED', payload: false });
                    dispatch({ type: 'SET_ONE_TIME_USER', payload: false });
                    dispatch({ type: 'SET_ORDER_ID', payload: null });
                    if (!rootState.logged) {
                        await AuthService.setAccessToken(nonUserToken.token);
                    }
                } catch (error) {
                    console.error("Logout error:", error);
                }
            }
        };

        checkOneTimeUser();
    }, []);

    return null; // This component does not render any UI elements, hence returning null
};

export default CartVerifyCtrl;

This TypeScript file uses React functional components with hooks to manage state and side effects. It assumes you have a Redux store (`RootState`) and services defined in your project structure. Adjust the imports and types according to your actual application setup.