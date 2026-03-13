/**
 * Service: LoginWidgetService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { login, updateProductAddress } from './actions/authActions'; // Adjust the import according to your project structure
import { getCartData } from './actions/cartActions'; // Adjust the import according to your project structure
import Notification from './components/Notification'; // Assuming you have a notification component
import { useNavigate } from 'react-router-dom';

const LoginWidgetService: React.FC = () => {
    const [loggedIn, setLoggedIn] = useState(false);
    const dispatch = useDispatch();
    const navigate = useNavigate();

    const handleLogin = async (credentials: any) => {
        try {
            const response = await dispatch(login(credentials));
            if (response.user && response.user.super) {
                Notification.success('Login successful'); // Adjust the translation method according to your project
                setLoggedIn(true);
                navigate('/dashboard'); // Assuming you have a dashboard route
            } else {
                const defaultAddressResponse = await dispatch(getDefaultAddress(1));
                if (defaultAddressResponse.response) {
                    const addressResponse = await dispatch(getAddress());
                    setAddresses(addressResponse.addresses);
                    setSenders(addressResponse.senders);
                }
            }
        } catch (error) {
            Notification.error('Wrong email or password'); // Adjust the error handling according to your project
        }
    };

    const handleUpdateProductAddress = async (product: any) => {
        try {
            const addressesResponse = await dispatch(reducePostData(product.addresses));
            const updateResponse = await dispatch(updateProductAddresses(product.orderID, product.productID, addressesResponse));
            if (updateResponse.response === true) {
                const patchData = {
                    orderID: product.orderID,
                    productID: product.productID,
                    productAddresses: product.addresses,
                };
                await dispatch(update(patchData));
                getCartData();
            }
        } catch (error) {
            console.error("Error updating product address:", error);
        }
    };

    useEffect(() => {
        if (!loggedIn) {
            const cartData = useSelector((state: any) => state.cart.data);
            if (cartData && cartData.carts) {
                cartData.carts.forEach((oneCart: any) => {
                    credentials.carts.push(oneCart._id);
                });
            }
            handleLogin(credentials);
        }
    }, [loggedIn]);

    return (
        <div>
            {/* Your component JSX */}
        </div>
    );
};

export default LoginWidgetService;