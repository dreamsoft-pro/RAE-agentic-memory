/**
 * Service: TaxService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import axios from 'axios';
import _ from 'lodash';
import { useRootStore } from './store'; // Assuming you have a root store or context for $rootScope

const TaxService = () => {
    const [getAllDef, setGetAllDef] = React.useState<any>(null);
    const cache = React.useMemo(() => ({}), []); // You might need to implement a proper caching mechanism
    const config = useRootStore().config; // Assuming you have access to your configuration store

    const getAll = async (force: boolean) => {
        if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
            setGetAllDef({ defer: true });
        } else {
            return getAllDef;
        }

        if (cache.get('collection') && !force) {
            getAllDef.resolve(cache.get('collection'));
        } else {
            try {
                const response = await axios({
                    method: 'GET',
                    url: `${config.API_URL}/tax`,
                });
                cache.put('collection', response.data);
                useRootStore().emit('Tax.getAll', response.data); // Assuming emit is a function in your store
                setGetAllDef({ resolve: response.data });
            } catch (error) {
                setGetAllDef({ reject: error });
            }
        }

        return getAllDef;
    };

    const create = async (lang: any) => {
        try {
            const response = await axios({
                method: 'POST',
                url: `${config.API_URL}/tax`,
                data: lang,
            });
            if (response.data.ID) {
                cache.remove('collection');
                return { resolve: response.data };
            } else {
                return { reject: response.data };
            }
        } catch (error) {
            return { reject: error };
        }
    };

    const update = async (lang: any) => {
        try {
            const response = await axios({
                method: 'PUT',
                url: `${config.API_URL}/tax`,
                data: lang,
            });
            if (response.data.response) {
                return { resolve: response.data };
            } else {
                return { reject: response.data };
            }
        } catch (error) {
            return { reject: error };
        }
    };

    const remove = async (id: string) => {
        try {
            const response = await axios({
                method: 'DELETE',
                url: `${config.API_URL}/tax/${id}`,
            });
            if (response.data.response) {
                return { resolve: response.data };
            } else {
                return { reject: response.data };
            }
        } catch (error) {
            return { reject: error };
        }
    };

    const getForProduct = async (groupID: string, typeID: string) => {
        try {
            const params = `?groupID=${groupID}`;
            if (typeID !== undefined) {
                // Assuming you can append more parameters here
            }
            const response = await axios({
                method: 'GET',
                url: `${config.API_URL}/tax/taxForProduct${params}`,
            });
            return { resolve: response.data };
        } catch (error) {
            return { reject: error };
        }
    };

    return { getAll, create, update, remove, getForProduct };
};

export default TaxService;