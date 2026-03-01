/**
 * Service: CalculationService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'next';
import axios, { AxiosPromise } from 'axios';

@Injectable()
export class CalculationService {
  private groupID: string;
  private typeID: string;

  constructor(groupID: string, typeID: string) {
    this.groupID = groupID;
    this.typeID = typeID;
  }

  getResource(): string {
    return ['ps_groups', this.groupID, 'ps_types', this.typeID, 'ps_calculate', 'calculatePublic'].join('/');
  }

  getVolumes(data: any): AxiosPromise<any> {
    const resource = this.getResource();
    return axios.patch(`${process.env.API_URL}${resource}`, data);
  }

  calculate(data: any): AxiosPromise<any> {
    const resource = this.getResource();
    return axios.post(`${process.env.API_URL}${resource}`, data);
  }

  saveCalculation(data: any): AxiosPromise<any> {
    const resource = ['ps_groups', this.groupID, 'ps_types', this.typeID, 'ps_calculate', 'saveCalculationPublic'].join('/');
    return axios.post(`${process.env.API_URL}${resource}`, data).then(response => {
      if (response.data.response) {
        return response;
      } else {
        throw new Error('No response from server');
      }
    });
  }

  updateName(data: any): AxiosPromise<any> {
    const resource = ['ps_groups', this.groupID, 'ps_types', this.typeID, 'ps_calculate', 'updateName', data.productID].join('/');
    return axios.patch(`${process.env.API_URL}${resource}`, data);
  }
}
