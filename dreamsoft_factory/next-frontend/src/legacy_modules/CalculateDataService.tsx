/**
 * Service: CalculateDataService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'react';
import axios, { AxiosPromise } from 'axios';
import { ConfigService } from './config.service'; // Assuming you have a config service for API URL

@Injectable({
  providedIn: 'root'
})
export class CalculateDataService {
  private typeID: string;
  private apiUrl: string;

  constructor(private configService: ConfigService) {
    this.apiUrl = this.configService.getApiUrl();
  }

  getResource(): string {
    return ['calculate', this.typeID].join('/');
  }

  getData(): AxiosPromise<any> {
    return axios({
      method: 'GET',
      url: `${this.apiUrl}${this.getResource()}`
    });
  }

  printOffer(data: any): AxiosPromise<any> {
    return axios({
      method: 'PATCH',
      url: `${this.apiUrl}calculate/printOffer`,
      data: data
    });
  }
}

This modernized code uses TypeScript and React's `axios` library for HTTP requests, assuming you have a configuration service to manage the API URL. The `CalculateDataService` is decorated with `@Injectable` from Angular's dependency injection system, which translates well into React's context or provider model if needed.