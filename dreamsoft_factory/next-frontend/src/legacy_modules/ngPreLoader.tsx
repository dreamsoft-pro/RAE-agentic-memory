/**
 * Service: ngPreLoader
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import React from 'react';
import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';

const NgPreLoader: React.FC<{ preloaderOn: boolean }> = ({ preloaderOn }) => {
  const [loaderSrc, setLoaderSrc] = useState('');
  const companyID = useSelector((state: any) => state.companyID);

  useEffect(() => {
    if (companyID) {
      setLoaderSrc(`${process.env.STATIC_URL}/${companyID}/images/pre-loader.gif`);
    } else {
      setLoaderSrc('');
    }
  }, [companyID]);

  return (
    <div className="pre-loader" style={{ display: preloaderOn ? 'block' : 'none' }}>
      <img loading="lazy" src={loaderSrc} alt="Pre Loader" />
    </div>
  );
};

export default NgPreLoader;