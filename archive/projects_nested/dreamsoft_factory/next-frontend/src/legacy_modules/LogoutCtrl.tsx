/**
 * Service: LogoutCtrl
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useRootStore } from '../stores/rootStore';
import { useNotification } from '../hooks/useNotification';
import { useAuthService } from '../services/authService';
import { useTokenService } from '../services/tokenService';
import { useLogoutService } from '../services/logoutService';

const LogoutCtrl: React.FC = () => {
    const router = useRouter();
    const rootStore = useRootStore();
    const notification = useNotification();
    const authService = useAuthService();
    const tokenService = useTokenService();
    const logoutService = useLogoutService();

    useEffect(() => {
        const init = async () => {
            try {
                const res = await authService.logout();
                if (res.logout) {
                    const data = await tokenService.getNonUserToken();
                    rootStore.setLogged(false);
                    rootStore.setOneTimeUser(false);
                    rootStore.setOrderID(null);
                    if (!rootStore.logged) {
                        notification.info('you_are_loggedout');
                        await authService.setAccessToken(data.token);
                        router.push('/login');
                    }
                } else {
                    notification.error('unexpected_error');
                }
            } catch (error) {
                notification.error('unexpected_error');
            }
        };

        init();
    }, [authService, tokenService, logoutService, rootStore, router, notification]);

    return null;
};

export default LogoutCtrl;
