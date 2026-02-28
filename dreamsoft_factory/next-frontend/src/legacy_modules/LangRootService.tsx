/**
 * Service: LangRootService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'next/types';
import axios, { AxiosPromise } from 'axios';
import { ConfigService } from './config.service'; // Assuming you have a config service for API URL

@Injectable({
  providedIn: 'root',
})
export class LangRootService {
  private resource = 'langroot';
  private apiUrl: string;

  constructor(private configService: ConfigService) {
    this.apiUrl = this.configService.getApiUrl();
  }

  getAll(): AxiosPromise<any> {
    return axios.get(`${this.apiUrl}/${this.resource}`);
  }

  getEmpty(): AxiosPromise<any> {
    return axios.get(`${this.apiUrl}/${this.resource}/showEmpty`);
  }

  create(lang: any): AxiosPromise<any> {
    return axios.post(`${this.apiUrl}/${this.resource}`, lang);
  }

  update(lang: any): AxiosPromise<any> {
    return axios.put(`${this.apiUrl}/${this.resource}`, lang).then((response) => {
      if (response.data.response) {
        return response;
      } else {
        throw new Error('Update failed');
      }
    });
  }

  remove(id: string): AxiosPromise<any> {
    return axios.delete(`${this.apiUrl}/${this.resource}/${id}`);
  }
}

This code is a modernized version of the provided AngularJS service, rewritten in TypeScript for Next.js. It uses `axios` for HTTP requests and assumes you have a configuration service to handle API URLs. The service methods (`getAll`, `getEmpty`, `create`, `update`, `remove`) are adapted to use promises and modern JavaScript syntax.