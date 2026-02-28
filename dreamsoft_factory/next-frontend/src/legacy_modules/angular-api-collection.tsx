/**
 * Service: angular-api-collection
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface ApiCollectionProps {
    collection: string;
    config?: {
        params?: { [key: string]: any };
        onSuccess?: (data: any) => void;
    };
}

const ApiCollection: React.FC<ApiCollectionProps> = ({ collection, config }) => {
    const [params, setParams] = useState({ limit: 10, offset: 0 });
    const [totalItems, setTotalItems] = useState(0);
    const [currentPage, setCurrentPage] = useState(1);
    const [totalPages, setTotalPages] = useState(0);

    useEffect(() => {
        fetchData();
    }, [params.limit, params.offset]);

    const fetchData = async () => {
        try {
            const response = await axios.get(`https://api.example.com/${collection}`, { params });
            setTotalItems(response.data.totalItems);
            setCurrentPage(response.data.current);
            setTotalPages(Math.ceil(response.data.totalItems / params.limit));
            if (config?.onSuccess) config.onSuccess(response.data);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    const setLimit = (val: number) => setParams({ ...params, limit: val });
    const getLimit = () => params.limit;
    const setPerPage = (perPage: number) => setLimit(perPage);
    const setOffset = (val: number) => setParams({ ...params, offset: val });
    const getOffset = () => params.offset;

    const calculateTotalPages = () => {
        setTotalPages(Math.ceil(totalItems / params.limit));
    };

    return (
        <div>
            {/* Render your collection data here */}
            <button onClick={() => setPrevPage()}>Previous Page</button>
            <button onClick={() => setNextPage()}>Next Page</button>
        </div>
    );
};

export default ApiCollection;
