/**
 * Service: CouponService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { ConfigService } from './config.service'; // Assuming you have a ConfigService for API URL

@Injectable({
  providedIn: 'root'
})
export class CouponService {
  private apiUrl: string;

  constructor(private http: HttpClient, private configService: ConfigService) {
    this.apiUrl = configService.getApiUrl();
  }

  getResource(): string[] {
    return ['dp_coupons'];
  }

  check(coupon: string, orderID: string): Observable<any> {
    const resource = this.getResource().concat(['check']);
    const url = `${this.apiUrl}/${resource.join('/')}`;
    const body = { coupon, orderID };

    return this.http.post(url, body).pipe(
      map((response: any) => response),
      catchError((error: any) => throwError(error))
    );
  }
}

This modernized code uses Angular's `HttpClient` for HTTP requests and TypeScript syntax. The `ConfigService` is assumed to be used for fetching the API URL, which should also be migrated if not already present in your Next.js/TypeScript project.