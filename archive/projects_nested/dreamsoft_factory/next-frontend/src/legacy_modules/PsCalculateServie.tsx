/**
 * Service: PsCalculateServie
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

Here's the modernized version of your AngularJS service `PsCalculateServie.js` converted to a Next.js/TypeScript file using React functional components and hooks for state management, along with Axios for HTTP requests:

import { createContext, useContext, useState } from 'react';
import axios, { AxiosError } from 'axios';

const ConfigContext = createContext({ API_URL: '' });

export const PsCalculateServiceProvider = ({ children, config }) => (
  <ConfigContext.Provider value={config}>
    {children}
  </ConfigContext.Provider>
);

export const usePsCalculateService = () => {
  const context = useContext(ConfigContext);
  if (!context) {
    throw new Error('usePsCalculateService must be used within a PsCalculateServiceProvider');
  }

  const [cache] = useState(() => ({}));

  const request = async (method: string, endpoint: string, data?: any) => {
    try {
      const url = `${context.API_URL}/ps_groups/${groupID}/ps_types/${typeID}/${endpoint}`;
      const response = await axios({ method, url, data });
      if (response.data.response) {
        return response.data;
      } else {
        throw response.data;
      }
    } catch (error: unknown) {
      if (axios.isAxiosError(error)) {
        throw error.response?.data || 'An unexpected error occurred';
      } else {
        throw error;
      }
    }
  };

  const calculate = async (item: any) => request('POST', '', item);
  const getVolumes = async (item: any) => request('PATCH', '', item);
  const saveCalculation = async (preparedProduct: any) => request('POST', 'saveCalculation', preparedProduct);

  return { calculate, getVolumes, saveCalculation };
};

This code assumes you are using React functional components and hooks for state management. The `PsCalculateServiceProvider` component provides the configuration context to its children, which includes the API URL. The custom hook `usePsCalculateService` manages the service logic including caching if needed, making HTTP requests with Axios, and handling responses or errors.

