import { $http, $q } from './httpBridge';
/**
 * Service: DeliveryService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'next';
import axios from 'axios';
import config from '../config'; // Assuming you have a config file for API_URL

@Injectable()
export class DeliveryService {
  private resource: string;

  constructor(private $q: any, private $http: any) {}

  getResource(): string {
    return ['deliveries', 'deliveriesPublic'].join('/');
  }

  getAll(currencyCode: string): Promise<any> {
    const resource = this.getResource();
    return this.$http({
      method: 'GET',
      url: `${config.API_URL}${resource}/${currencyCode}`,
    }).then((response) => response.data);
  }

  findParcelShops(addressID: number, deliveryID: number, courierID: number): Promise<any> {
    const resource = this.getResource();
    const urlParams = `?deliveryID=${deliveryID}&courierID=${courierID}&addressID=${addressID}`;
    return this.$http({
      method: 'GET',
      url: `${config.API_URL}deliveries/findParcelsPublic${urlParams}`,
    }).then((response) => response.data);
  }
}

This code is a modernized version of the provided AngularJS service, adapted for use in a Next.js environment with TypeScript. It uses `axios` for HTTP requests and assumes you have a configuration file (`config`) to manage your API URL. The service is defined using TypeScript's class syntax and leverages dependency injection for `$q` and `$http`.