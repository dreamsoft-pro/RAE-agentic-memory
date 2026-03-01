/**
 * Service: HomepageBannerService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { injectable } from 'inversify';
import { Restangular } from 'restangular';
import { AxiosInstance } from 'axios';
import { config } from '../config';
import { defer, from, Observable } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@injectable()
export class HomepageBannerService {
  private http: AxiosInstance;
  private apiUrl: string;

  constructor(private restangular: Restangular) {
    this.http = restangular.service('httpClient');
    this.apiUrl = config.API_URL;
  }

  public getAll(): Observable<any> {
    const resource = 'homePageBanner';
    return from(this.http.get(`${this.apiUrl}${resource}/homePageBannerPublic`)).pipe(
      map((response) => response.data),
      catchError((error) => {
        console.error('Error fetching homepage banner:', error);
        return defer(() => Promise.reject(error));
      })
    );
  }
}
