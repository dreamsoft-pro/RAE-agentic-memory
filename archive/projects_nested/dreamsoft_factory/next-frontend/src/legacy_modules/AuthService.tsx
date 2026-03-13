/**
 * Service: AuthService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import _ from 'lodash';
import { useRootStore } from './store'; // Assuming you have a root store or context for global state management

const AuthService: React.FC = () => {
    const [logged, setLogged] = useState(false);
    const { userData, setUserData } = useRootStore();

    useEffect(() => {
        const checkAuth = async () => {
            const token = await getAccessToken();
            if (token) {
                const currentUser = await getCurrentUser();
                if (_.isObject(currentUser) && !_.isEmpty(currentUser)) {
                    setLogged(true);
                }
            }
        };
        checkAuth();
    }, []);

    const getAccessToken = async () => {
        // Implement your access token retrieval logic here
        return null;
    };

    const getCurrentUser = async () => {
        // Implement your current user retrieval logic here
        return {};
    };

    const handleLogin = async (credentials: { email: string, name: string, lastName: string }) => {
        try {
            const response = await axios.post($config.AUTH_URL + 'login', credentials, {
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            });
            if (response.data) {
                setUserData(response.data);
                setLogged(true);
                return response.data;
            }
        } catch (error) {
            console.error('Login failed:', error);
        }
    };

    const handleLogout = async () => {
        try {
            await axios.get($config.AUTH_URL + 'logout');
            setLogged(false);
        } catch (error) {
            console.error('Logout failed:', error);
        }
    };

    return (
        <div>
            {logged ? (
                <button onClick={handleLogout}>Logout</button>
            ) : (
                <button onClick={() => handleLogin({ email: '', name: '', lastName: '' })}>Login</button>
            )}
        </div>
    );
};

export default AuthService;