/**
 * Service: PsAttributeService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { useState, useEffect, useRef } from 'react';
import { createRestangular } from 'restangular';
import axios from 'axios';

const cacheFactory = require('cache-factory'); // Assuming you have a similar caching mechanism in TypeScript

interface AttributeServiceProps {
    groupID: string;
    typeID: string;
}

function PsAttributeService({ groupID, typeID }: AttributeServiceProps) {
    const [data, setData] = useState<any>(null);
    const cache = useRef(cacheFactory('ps_product_options'));
    const restangular = createRestangular();
    const config = useConfig(); // Assuming you have a similar configuration setup in TypeScript

    useEffect(() => {
        fetchData();
    }, []);

    async function fetchData(force: boolean = false) {
        if (cache.current.get(`ps_groups/${groupID}/ps_types/${typeID}/ps_product_options`) && !force) {
            setData(cache.current.get(`ps_groups/${groupID}/ps_types/${typeID}/ps_product_options`));
        } else {
            try {
                const response = await restangular.all(`ps_groups/${groupID}/ps_types/${typeID}/ps_product_options`).getList();
                cache.current.put(`ps_groups/${groupID}/ps_types/${typeID}/ps_product_options`, response.plain());
                setData(response.plain());
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        }
    }

    return { data }; // Return the fetched data or other relevant state information
}

function useConfig() {
    return { API_URL: 'your-api-url' }; // Implement your configuration hook here
}