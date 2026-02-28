import { $q } from './httpBridge';
/**
 * Service: PsPageService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

Here's the modernized version of your AngularJS service `PsPageService` converted to TypeScript and used in a Next.js/TSX environment:

import { Restangular } from 'restangular';
import { $q } from 'ngimport'; // Assuming ngimport is used for $q in non-Angular environments like React with hooks
import { useEffect, useState } from 'react';

interface IPageService {
    groupID: string;
    typeID: string;
    getPublic: (force?: boolean) => Promise<any>;
    getCustomNames: () => Promise<any>;
}

const usePageService = (groupID: string, typeID: string): IPageService => {
    const [data, setData] = useState(null);
    const cache = $q.defer();

    const fetchData = async (force: boolean) => {
        if (!force && data) {
            return data;
        } else {
            try {
                const result = await Restangular.all('ps_groups/' + groupID + '/ps_types/' + typeID + '/ps_pages').getList();
                setData(result.plain());
                return result.plain();
            } catch (error) {
                console.error("Error fetching data:", error);
                throw error;
            }
        }
    };

    useEffect(() => {
        fetchData(false);
    }, [groupID, typeID]);

    const getPublic: IPageService['getPublic'] = async (force) => {
        return await fetchData(force || false);
    };

    const getCustomNames: IPageService['getCustomNames'] = async () => {
        try {
            const result = await Restangular.all('ps_pages').one('customName', typeID).get();
            setData(result.plain());
            return result.plain();
        } catch (error) {
            console.error("Error fetching custom names:", error);
            throw error;
        }
    };

    return { groupID, typeID, getPublic, getCustomNames };
};

export default usePageService;

This TypeScript code defines a React hook `usePageService` that acts as a modernized version of your AngularJS service. It uses hooks and async/await for asynchronous operations, and it's designed to be used in a Next.js or similar environment where you might not have direct access to Angular services like `$q`.

Please note that this code assumes the use of Restangular as a hypothetical example. You would need to adjust imports and configurations according to your actual setup in a Next.js/React application.