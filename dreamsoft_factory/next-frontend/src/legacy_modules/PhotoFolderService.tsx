/**
 * Service: PhotoFolderService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

Here is the modernized version of your JavaScript file (`PhotoFolderService.tsx`) using TypeScript and React-like syntax conventions:

import { useState, useEffect } from 'react';
import axios from 'axios';

interface PhotoFolderServiceProps {
    url: string;
    header: any;
}

const PhotoFolderService = ({ url, header }: PhotoFolderServiceProps) => {
    const [responseData, setResponseData] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        // Example function to get image by extension
        const getImageByExtension = async (id: string, extension: string) => {
            try {
                const res = await axios.get(`${url}get-image-in-extension/${id}/${extension}`, { headers: header });
                setResponseData(res.data);
            } catch (err) {
                setError(err.response ? err.response.status : 'Network Error');
            }
        };

        // Example function to get projects for types
        const getProjectsForTypes = async (formats: string[]) => {
            try {
                const res = await axios.get(`${url}getProjectsForTypes`, { headers: header });
                setResponseData(res.data);
            } catch (err) {
                setError(err.response ? err.response.status : 'Network Error');
            }
        };

        // Example function to get URL image by extension
        const getUrlImageByExtension = (id: string, extension: string) => {
            return `${url}get-image-in-extension/${id}/${extension}`;
        };

        // You can call these functions as needed in your application
    }, [url, header]);

    return { getImageByExtension, getProjectsForTypes, getUrlImageByExtension };
};

export default PhotoFolderService;

This TypeScript file uses modern JavaScript/TypeScript syntax and features such as `useState`, `useEffect` for state and effect management from React hooks. It also utilizes `axios` for making HTTP requests, which is a common practice in modern web development. The functions are defined within the component to encapsulate their functionality, and they use async/await for asynchronous operations.