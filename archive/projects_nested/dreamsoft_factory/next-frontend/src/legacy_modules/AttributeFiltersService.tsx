/**
 * Service: AttributeFiltersService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { createContext, useContext, useState, useEffect, useRef } from 'react';
import axios, { AxiosError, AxiosResponse } from 'axios';

interface Config {
  API_URL: string;
}

const AttributeFiltersServiceContext = createContext<any>(null);

export const useAttributeFiltersService = () => useContext(AttributeFiltersServiceContext);

export const AttributeFiltersServiceProvider: React.FC<{ config: Config }> = ({ children, config }) => {
  const [data, setData] = useState<any>(null);
  const isMounted = useRef(true);

  useEffect(() => {
    return () => {
      isMounted.current = false;
    };
  }, []);

  const fetchData = async (url: string, method: 'GET' | 'POST', data?: any) => {
    try {
      const response: AxiosResponse = await axios({
        method,
        url: `${config.API_URL}${url}`,
        data,
      });
      if (isMounted.current) setData(response.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const getAttributeFilters = async (attrID: string) => {
    await fetchData(['attributeFilters', attrID].join('/'), 'GET');
  };

  const getProductsUsingOptions = async (attrID: string) => {
    await fetchData(['productsUsingOptions', attrID].join('/'), 'GET');
  };

  const getOptions = async (attrID: string) => {
    await fetchData(['attributeOptions', attrID].join('/'), 'GET');
  };

  const getOption = async (data: any) => {
    await fetchData('attributeOption', 'POST', data);
  };

  const getRelativePapers = async (data: any) => {
    await fetchData('getRelativePapers', 'POST', data);
  };

  const search = async (attrID: string, filter: any) => {
    await fetchData(['attributeFilters', attrID].join('/'), 'POST', filter);
  };

  const downloadPDF = async (data: any) => {
    await fetchData('attributeOptionPDF', 'POST', data);
  };

  return (
    <AttributeFiltersServiceContext.Provider value={{ getAttributeFilters, getProductsUsingOptions, getOptions, getOption, getRelativePapers, search, downloadPDF }}>
      {children}
    </AttributeFiltersServiceContext.Provider>
  );
};