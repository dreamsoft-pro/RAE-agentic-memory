/**
 * Service: CustomProductService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'next';
import axios, { AxiosPromise } from 'axios';

@Injectable()
export class CustomProductService {
  private resource = 'dp_customProducts';

  constructor(private config: any) {}

  getUploadUrl(customProductID: string): string {
    return `${this.config.API_URL}/${this.resource}/files/${customProductID}`;
  }

  add(data: any): AxiosPromise<any> {
    return axios({
      method: 'POST',
      url: `${this.config.API_URL}/${this.resource}`,
      data: data,
    });
  }
}
