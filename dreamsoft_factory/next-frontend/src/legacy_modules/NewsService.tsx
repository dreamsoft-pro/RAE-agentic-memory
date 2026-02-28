/**
 * Service: NewsService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import axios from 'axios';
import { Config } from '../config/Config'; // Assuming you have a config file for API URL

export class NewsService {
  private resource: string = 'dp_news';

  public getRss(data: any) {
    const url = `${Config.API_URL}/${this.resource}/rss`;
    return axios.get(url)
      .then((response) => response.data)
      .catch((error) => {
        throw error;
      });
  }
}
