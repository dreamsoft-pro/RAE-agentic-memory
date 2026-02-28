/**
 * Service: CalcFileService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { useState } from 'react';
import axios from 'axios';

interface CalcFileServiceProps {
  API_URL: string;
}

const CalcFileService = ({ API_URL }: CalcFileServiceProps) => {
  const [state, setState] = useState({ loading: false, error: null, data: null });

  const request = async (method: 'GET' | 'POST' | 'DELETE', url: string, data?: any) => {
    try {
      setState((prev) => ({ ...prev, loading: true }));
      const response = await axios({ method, url, data });
      setState((prev) => ({ ...prev, data: response.data }));
    } catch (error) {
      setState((prev) => ({ ...prev, error }));
    } finally {
      setState((prev) => ({ ...prev, loading: false }));
    }
  };

  const getUrl = (typeID: string): string => `${API_URL}/dp_products/${typeID}/calcFilesUploader`;

  const getAllByType = async (typeID: string) => {
    const url = getUrl(typeID);
    await request('GET', url);
  };

  const removeFile = async (typeID: string, fileID: string) => {
    const url = `${getUrl(typeID)}/${fileID}`;
    await request('DELETE', url);
  };

  // Add other methods similarly...

  return {
    getAllByType,
    removeFile,
    // ...other methods
  };
};

export default CalcFileService;