/**
 * Service: LoadingService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

// LoadingService.tsx
import { useState, useEffect } from 'react';

const LoadingService = () => {
  const [loadingCount, setLoadingCount] = useState(0);
  const [errorCount, setErrorCount] = useState(0);

  const isLoading = () => loadingCount > 0;

  const requested = () => setLoadingCount((prev) => prev + 1);

  const responsed = (status: number) => {
    if (status !== 200 && status !== 401) {
      setErrorCount((prev) => prev + 1);
    }
    setLoadingCount((prev) => prev - 1);
  };

  const countError = () => setErrorCount((prev) => prev + 1);

  const getCount = () => loadingCount;

  const getErrorCount = () => errorCount;

  return {
    isLoading,
    requested,
    responsed,
    countError,
    getCount,
    getErrorCount,
  };
};

export default LoadingService;
