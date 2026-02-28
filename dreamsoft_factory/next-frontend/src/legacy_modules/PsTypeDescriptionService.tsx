/**
 * Service: PsTypeDescriptionService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'next/types';
import axios, { AxiosPromise } from 'axios';
import { Config } from '../config'; // Assuming you have a config file for API_URL

@Injectable({
  providedIn: 'root',
})
export class PsTypeDescriptionService {
  constructor(private readonly config: Config) {}

  async getAll(groupID: string, typeID: string): Promise<any> {
    const apiUrl = this.config.API_URL;
    try {
      const response: AxiosPromise = await axios({
        method: 'GET',
        url: `${apiUrl}ps_typeDescriptions/typeDescriptionsPublic?groupID=${groupID}&typeID=${typeID}`,
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching type descriptions:', error);
      throw error;
    }
  }
}
