/**
 * Service: ngMainPreLoader
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React, { useState, useEffect } from 'react';
import LoadingService from './LoadingService'; // Adjust the import according to your project structure

const MainPreLoader: React.FC = () => {
  const [showPreloader, setShowPreloader] = useState(false);
  const [loadingCount, setLoadingCount] = useState(0);
  const [errorCount, setErrorCount] = useState(0);

  useEffect(() => {
    const loadingStartListener = () => {
      const count = LoadingService.count();
      if (count > 2) {
        setTimeout(() => setShowPreloader(true), 2000);
      } else {
        setShowPreloader(true);
      }
    };

    const loadingFinishListener = () => {
      const count = LoadingService.count();
      const errorCount = LoadingService.errorCount();
      if (count === 0) {
        setShowPreloader(false);
      }
      setErrorCount(errorCount);
    };

    document.addEventListener('loading:start', loadingStartListener);
    document.addEventListener('loading:finish', loadingFinishListener);

    return () => {
      document.removeEventListener('loading:start', loadingStartListener);
      document.removeEventListener('loading:finish', loadingFinishListener);
    };
  }, []);

  return (
    <div id="mainLoader" className={showPreloader ? '' : 'finished'}>
      <div className="main-pre-loader">
        <span></span>
      </div>
      {loadingCount}
      {errorCount > 0 && <span style={{ color: 'red', padding: '4px', position: 'fixed', right: 0 }}>errors: {errorCount}</span>}
    </div>
  );
};

export default MainPreLoader;