/**
 * Service: RealizationTimeService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { RestangularProvider, Restangular } from 'restangular';
import { useConfig } from './configContext';
import { useCacheFactory } from './cacheContext';

const RealizationTimeService = () => {
    const config = useConfig();
    const cache = useCacheFactory('ps_realizationTimes');
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const fetchData = async (force) => {
        if (cache.get('collection') && !force) {
            setData(cache.get('collection'));
        } else {
            try {
                const response = await Restangular.all('ps_realizationTimes').getList();
                if (response) {
                    cache.put('collection', response.plain());
                    setData(response.plain());
                } else {
                    throw new Error('No data found');
                }
            } catch (err) {
                setError(err);
            }
        }
    };

    const editItem = async (item) => {
        try {
            const response = await Restangular.all('ps_realizationTimes').customPUT(item);
            if (response.response) {
                cache.remove('collection');
                setData(response);
            } else {
                throw new Error('Failed to update item');
            }
        } catch (err) {
            setError(err);
        }
    };

    const addItem = async (item) => {
        try {
            const response = await Restangular.all('ps_realizationTimes').doPOST(item);
            if (response.ID) {
                cache.remove('collection');
                setData(response.plain());
            } else {
                throw new Error('Failed to add item');
            }
        } catch (err) {
            setError(err);
        }
    };

    const sortItems = async (sort) => {
        try {
            const response = await axios({
                method: 'PATCH',
                url: `${config.API_URL}/ps_realizationTimes/sort`,
                data: sort,
            });
            if (response.data.response) {
                setData(response.data);
            } else {
                throw new Error('Failed to sort items');
            }
        } catch (err) {
            setError(err);
        }
    };

    const removeItem = async (item) => {
        try {
            const response = await Restangular.all('ps_realizationTimes').one(item.ID + '').remove();
            if (response.response) {
                cache.remove('collection');
                setData(response.plain());
            } else {
                throw new Error('Failed to remove item');
            }
        } catch (err) {
            setError(err);
        }
    };

    return { fetchData, editItem, addItem, sortItems, removeItem };
};

export default RealizationTimeService;