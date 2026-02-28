/**
 * Service: SettingService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { $config } from './config'; // Assuming this is your config module

interface SettingServiceProps {
  module: string;
}

const SettingService: React.FC<SettingServiceProps> = ({ module }) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const isMounted = useRef(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(`${$config.API_URL}/settings/getPublicSettings/${module}`);
        if (isMounted.current) {
          setData(response.data);
        }
      } catch (err) {
        if (isMounted.current) {
          setError(err);
        }
      }
    };

    fetchData();

    return () => {
      isMounted.current = false;
    };
  }, [module]);

  if (error) {
    return <div>Error: {error.message}</div>;
  }

  return (
    <div>
      {data ? (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default SettingService;