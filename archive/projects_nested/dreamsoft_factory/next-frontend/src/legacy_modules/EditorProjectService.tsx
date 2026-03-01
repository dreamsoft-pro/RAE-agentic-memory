/**
 * Service: EditorProjectService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

/**
 */
import React, { createContext, useContext, useState, useEffect, useRef } from 'react';
import axios from 'axios';

const ConfigContext = createContext<any>(null);

export const EditorProjectService: React.FC = () => {
    const config = useContext(ConfigContext);
    const [accessTokenName] = useState(config.ACCESS_TOKEN_NAME);
    const [header, setHeader] = useState({});

    useEffect(() => {
        const token = AuthService.readCookie(accessTokenName);
        if (token) {
            setHeader((prevHeader) => ({ ...prevHeader, [accessTokenName]: token }));
        }
    }, [accessTokenName]);

    const getProjectPrev = async (projectID: string) => {
        try {
            const response = await axios.get(`${config.API_URL}jpgPreview?projectID=${projectID}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    };

    const shareMyProject = async (email: string, projectID: string) => {
        try {
            const response = await $.ajax({
                url: `${config.API_URL}shareMyProject/${projectID}`,
                type: 'POST',
                headers: header,
                data: { emails: [email] },
                crossDomain: true,
                withCredentials: true,
            });
            return response;
        } catch (error) {
            throw error.status;
        }
    };

    const shareMyProjectByFb = async (projectID: string) => {
        try {
            const response = await $.ajax({
                url: `${config.API_URL}getsharedProjectFromFB/${projectID}`,
                type: 'POST',
                headers: header,
                crossDomain: true,
                withCredentials: true,
            });
            return response;
        } catch (error) {
            throw error.status;
        }
    };

    const getProjectsData = async (projects: any[]) => {
        try {
            const response = await $.ajax({
                url: `${config.API_URL}getProjectsData`,
                type: 'POST',
                headers: header,
                data: { projects },
                crossDomain: true,
                withCredentials: true,
            });
            return response;
        } catch (error) {
            throw error.status;
        }
    };

    return null; // This should be a React component that uses these functions and returns JSX
};

export const ConfigProvider: React.FC<{ config: any, children: React.ReactNode }> = ({ config, children }) => {
    return <ConfigContext.Provider value={config}>{children}</ConfigContext.Provider>;
};