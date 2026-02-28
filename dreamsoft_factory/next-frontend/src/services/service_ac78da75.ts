import axios from 'axios';
import { useEffect } from 'next/hooks';
import { useState } from 'react';

interface Credentials {
    username: string;
    password: string;
    orderID?: string;
    carts?: any[];
}

const loginInCart = (scope: any, credentials: Credentials, onetime: boolean = false) => {
    const [promiseResolver, setPromiseResolver] = useState<{ resolve: Function }>();

    useEffect(() => {
        if (_.isEmpty(credentials)) {
            Notification.error($filter('translate')('unexpected_error'));
            return;
        }

        AuthService.getSessionCarts().then((cartData) => {
            credentials.orderID = cartData?.orderID || '';
            credentials.carts = [];

            if (cartData && cartData.carts) {
                _.each(cartData.carts, function(oneCart) {
                    // Process each cart
                });
            }

            promiseResolver.resolve(true);
        }).catch(() => {
            promiseResolver.resolve(false);
        });

        return () => {
            setPromiseResolver(undefined);
        };
    }, [credentials]);

    const def = (resolve: Function) => setPromiseResolver({ resolve });
    return new Promise(def);
};