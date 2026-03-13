/**
 * Service: DpOrderService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { createContext, useContext, useState, useEffect, useRef } from 'react';
import axios from 'axios';

interface DpOrderServiceProps {
  API_URL: string;
}

const DpOrderServiceContext = createContext<DpOrderServiceProps | null>(null);

export const useDpOrderService = () => {
  return useContext(DpOrderServiceContext);
};

interface DpOrderServiceInterface {
  getAll: () => Promise<any>;
  get: (id: string) => Promise<any>;
  edit: (id: string, data: any) => Promise<any>;
  sellerNotReady: () => Promise<any>;
  getMyZone: (params?: any) => Promise<any>;
  getMyZoneCount: (params?: any) => Promise<any>;
  sendPaymentSuccess: (data: any, orderID: string) => Promise<any>;
  recalculateDelivery: (params: any) => Promise<any>;
  addToJoinedDelivery: (addressID: string, currency: string) => Promise<any>;
  changeAddresses: (orderID: string, productID: string, productAddresses: any) => Promise<any>;
  rejectOffer: (data: any) => Promise<any>;
  changeMultiOffer: (data: any) => Promise<any>;
}

const DpOrderService = (): DpOrderServiceInterface => {
  const API_URL = useDpOrderService()?.API_URL || '';

  const getAll = async () => {
    const def = axios.CancelToken.source();
    try {
      const response = await axios.get(`${API_URL}/dp_orders`, { cancelToken: def.token });
      return Promise.resolve(response.data);
    } catch (error) {
      return Promise.reject(error);
    }
  };

  const get = async (id: string) => {
    try {
      const response = await axios.get(`${API_URL}/dp_orders/${id}`);
      return Promise.resolve(response.data);
    } catch (error) {
      return Promise.reject(error);
    }
  };

  const edit = async (id: string, data: any) => {
    try {
      const response = await axios.put(`${API_URL}/dp_orders/${id}`, data);
      return Promise.resolve(response.data);
    } catch (error) {
      return Promise.reject(error);
    }
  };

  const sellerNotReady = async () => {
    try {
      const response = await axios.get(`${API_URL}/dp_orders/sellerNotReady`);
      return Promise.resolve(response.data);
    } catch (error) {
      return Promise.reject(error);
    }
  };

  // Implement other methods similarly...

  return {
    getAll,
    get,
    edit,
    sellerNotReady,
    getMyZone,
    getMyZoneCount,
    sendPaymentSuccess,
    recalculateDelivery,
    addToJoinedDelivery,
    changeAddresses,
    rejectOffer,
    changeMultiOffer,
  };
};

const DpOrderServiceProvider: React.FC = ({ children }) => {
  const [API_URL] = useState('your-api-url');
  return (
    <DpOrderServiceContext.Provider value={{ API_URL }}>
      {children}
    </DpOrderServiceContext.Provider>
  );
};

export default DpOrderServiceProvider;