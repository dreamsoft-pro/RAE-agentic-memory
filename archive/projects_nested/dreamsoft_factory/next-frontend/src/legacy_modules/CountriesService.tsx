/**
 * Service: CountriesService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'next-core';
import axios, { AxiosPromise } from 'axios';

@Injectable('digitalprint.services')
export class CountriesService {
  private API_URL = ''; // Assuming you have a way to set this in Next.js environment variables or config

  constructor(private $rootScope: any, private $config: any) {}

  getResource(): string {
    return ['dp_countries'].join('/');
  }

  getAll(): AxiosPromise<any> {
    const resource = this.getResource();
    return axios({
      method: 'GET',
      url: `${this.API_URL}${resource}`,
    });
  }
}
