/**
 * Service: CountService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'react';
import axios, { AxiosPromise } from 'axios';

@Injectable({
  providedIn: 'root',
})
export class CountService {
  private resource = 'dp_calculate';

  reCalculateCart(data: any): Promise<any> {
    return this.makeRequest('PATCH', data, `${this.resource}/cartReCalculate`);
  }

  restorePricesCart(data: any): Promise<any> {
    return this.makeRequest('PATCH', data, `${this.resource}/cartRestorePrices`);
  }

  private makeRequest(method: string, data: any, urlSuffix: string): Promise<any> {
    const apiUrl = process.env.API_URL; // Assuming environment variables are managed in a .env file or similar
    const requestConfig = {
      method,
      data,
      url: `${apiUrl}/${urlSuffix}`,
    };

    return axios(requestConfig)
      .then((response) => response.data)
      .catch((error) => {
        throw error;
      });
  }
}

This modernized code uses TypeScript and React's `axios` library for HTTP requests, which is a common approach in Next.js applications using TypeScript. The service is decorated with `@Injectable` to indicate that it can be provided at the root level of dependency injection, similar to how Angular services are managed.