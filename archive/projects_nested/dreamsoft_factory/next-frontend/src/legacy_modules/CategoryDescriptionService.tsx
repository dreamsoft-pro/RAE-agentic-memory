/**
 * Service: CategoryDescriptionService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'react';
import axios from 'axios';
import config from '../config'; // Assuming you have a config file for API URL

@Injectable({
  providedIn: 'root',
})
export class CategoryDescriptionService {
  constructor() {}

  async getAll(list: string) {
    try {
      const response = await axios.get(`${config.API_URL}categoriesDescriptions/categoriesDescriptionsPublic?list=${list}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching category descriptions:', error);
      throw error;
    }
  }
}
