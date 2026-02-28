/**
 * Service: DpOrderStatusService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

// FILE: DpOrderStatusService.tsx (chunk 0/1)
import { Injectable } from 'react';
import axios, { AxiosPromise } from 'axios';
import { ConfigService } from './configService'; // Assuming you have a ConfigService for API URL

@Injectable({
  providedIn: 'root',
})
export class DpOrderStatusService {
  private resource = 'dp_statuses';
  private apiUrl: string;

  constructor(private configService: ConfigService) {
    this.apiUrl = this.configService.getApiUrl();
  }

  public getAll(active: boolean): AxiosPromise<any> {
    return axios({
      method: 'GET',
      url: `${this.apiUrl}/${this.resource}/forClient`,
    });
  }
}
