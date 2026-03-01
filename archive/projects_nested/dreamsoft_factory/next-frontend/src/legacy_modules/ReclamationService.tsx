/**
 * Service: ReclamationService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

/**
 */

import { useState, useEffect } from 'react';
import axios from 'axios';

const ReclamationService = () => {
    const [data, setData] = useState(null);
    const [error, setError] = useState(null);

    const fetchData = async (url: string, method: string) => {
        try {
            const response = await axios({
                method: method,
                url: url,
            });
            setData(response.data);
        } catch (err) {
            setError(err);
        }
    };

    return { data, error, fetchData };
};

const ReclamationServiceComponent = () => {
    const faultsResource = 'dp_reclamation_faults';
    const resource = 'dp_reclamations';
    const messagesResource = 'dp_reclamations_messages';

    const { data: faultsData, error: faultsError, fetchData: fetchFaults } = ReclamationService();
    const { data: messagesData, error: messagesError, fetchData: fetchMessages } = ReclamationService();

    useEffect(() => {
        fetchFaults(`${API_URL}/${faultsResource}`);
    }, [fetchFaults]);

    const getUploadUrl = (reclamationID: string) => `${API_URL}/${resource}/files/${reclamationID}`;

    const addReclamation = async (data: any, orderID: string) => {
        try {
            const response = await axios({
                method: 'POST',
                url: `${API_URL}/${resource}/${orderID}`,
                data: data,
            });
            return response.data;
        } catch (err) {
            throw err;
        }
    };

    const findByOrder = async (orderID: string) => {
        try {
            const response = await axios({
                method: 'GET',
                url: `${API_URL}/${messagesResource}/myZone/${reclamationID}`,
            });
            return response.data;
        } catch (err) {
            throw err;
        }
    };

    const getFiles = async (reclamationID: string) => {
        try {
            const response = await axios({
                method: 'GET',
                url: `${API_URL}/${resource}/getFiles/${reclamationID}`,
            });
            return response.data;
        } catch (err) {
            throw err;
        }
    };

    const getAll = async (params?: any) => {
        try {
            const response = await axios({
                method: 'GET',
                url: `${API_URL}/${resource}/myZone`,
                params: params,
            });
            return response.data;
        } catch (err) {
            throw err;
        }
    };

    const getMyZoneCount = async (params?: any) => {
        try {
            const response = await axios({
                method: 'GET',
                url: `${API_URL}/${resource}/myZoneCount`,
                params: params,
            });
            return response.data;
        } catch (err) {
            throw err;
        }
    };

    const getMessages = async (reclamationID: string) => {
        try {
            const response = await axios({
                method: 'GET',
                url: `${API_URL}/${messagesResource}/myZone/${reclamationID}`,
            });
            return response.data;
        } catch (err) {
            throw err;
        }
    };

    return (
        <div>
            {/* Use the functions here */}
        </div>
    );
};

export default ReclamationServiceComponent;