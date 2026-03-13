/**
 * Service: CurrencyRootService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import _ from 'lodash';
import { useRootStore } from './store'; // Assuming you have a store or context for global state

const CurrencyRootService = () => {
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | null>(null);
    const cache = useRef(null);
    const resource = 'currencyroot';
    const API_URL = process.env.REACT_APP_API_URL;

    useEffect(() => {
        if (_.isNull(data) || loading || data.promise.$$state.status === 1) {
            getData();
        }
    }, [data, loading]);

    const getData = async () => {
        setLoading(true);
        try {
            if (cache.current && !loading) {
                setData(cache.current);
            } else {
                const response = await axios({
                    method: 'GET',
                    url: `${API_URL}/${resource}`,
                });
                cache.current = response.data;
                useRootStore().emit('CurrencyRoot.getAll', response.data);
                setData(response.data);
            }
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const create = async (lang: any) => {
        try {
            const response = await axios({
                method: 'POST',
                url: `${API_URL}/${resource}`,
                data: lang,
            });
            if (response.data.ID) {
                cache.current = null; // Assuming you need to clear the cache or update it
            }
            return response.data;
        } catch (err) {
            throw err;
        }
    };

    const update = async (lang: any) => {
        try {
            const response = await axios({
                method: 'PUT',
                url: `${API_URL}/${resource}`,
                data: lang,
            });
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Update failed');
            }
        } catch (err) {
            throw err;
        }
    };

    const remove = async (id: string) => {
        try {
            const response = await axios({
                method: 'DELETE',
                url: `${API_URL}/${resource}/${id}`,
            });
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Remove failed');
            }
        } catch (err) {
            throw err;
        }
    };

    return { data, loading, error, getAll: getData, create, update, remove };
};

export default CurrencyRootService;