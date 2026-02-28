import { $q } from './httpBridge';
/**
 * Service: LangSettingsService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import _ from 'lodash';
import { useRootScope, useConfig } from './hooks'; // Assuming these are custom hooks you've defined for Angular-like services in a React context

const LangSettingsService = () => {
    const [getAllDef, setGetAllDef] = useState<any>(null);
    const cacheRef = useRef({});
    const $rootScope = useRootScope();
    const $config = useConfig();

    const resource = 'langsettings';
    const cache = cacheRef.current[resource] || ($cacheFactory(resource) as any);

    useEffect(() => {
        if (_.isNull(getAllDef) || getAllDef?.promise?.$$state?.status === 1) {
            setGetAllDef($q.defer());
        } else {
            return getAllDef;
        }

        const fetchData = async () => {
            if (cache.get('collection') && !force) {
                const data = cache.get('collection');
                $rootScope.$emit('LangSettings.getAll', data);
                setGetAllDef(data);
            } else {
                try {
                    const response = await axios({
                        method: 'GET',
                        url: `${$config.API_URL}${resource}`,
                    });
                    cache.put('collection', response.data);
                    $rootScope.$emit('LangSettings.getAll', response.data);
                    setGetAllDef(response.data);
                } catch (error) {
                    console.error("Error fetching data:", error);
                    setGetAllDef(error);
                }
            }
        };

        fetchData();
    }, [getAllDef, $config, resource, cache]);

    const getAll = async (force: boolean) => {
        if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
            setGetAllDef($q.defer());
        } else {
            return getAllDef;
        }
    };

    const create = async (lang: any) => {
        try {
            const response = await axios({
                method: 'POST',
                url: `${$config.API_URL}${resource}`,
                data: lang,
            });
            if (response.data.ID) {
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error("Failed to create");
            }
        } catch (error) {
            console.error("Error creating data:", error);
            throw error;
        }
    };

    const update = async (lang: any) => {
        try {
            const response = await axios({
                method: 'PUT',
                url: `${$config.API_URL}${resource}`,
                data: lang,
            });
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error("Failed to update");
            }
        } catch (error) {
            console.error("Error updating data:", error);
            throw error;
        }
    };

    const remove = async (id: any) => {
        try {
            const response = await axios({
                method: 'DELETE',
                url: `${$config.API_URL}${resource}/${id}`,
            });
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error("Failed to remove");
            }
        } catch (error) {
            console.error("Error removing data:", error);
            throw error;
        }
    };

    return { getAll, create, update, remove };
};

export default LangSettingsService;