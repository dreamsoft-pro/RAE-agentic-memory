/**
 * Service: TokenService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable, Injector } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, defer, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class TokenService {
  private http: HttpClient;

  constructor(private injector: Injector) {}

  check(): Observable<any> {
    this.http = this.injector.get(HttpClient);
    const url = `${$config.API_URL}/auth/check`;
    return this.http.get(url).pipe(
      map((data: any) => {
        if (data.response) {
          return data;
        } else {
          throw data;
        }
      }),
      catchError((error: any) => throwError(error))
    );
  }

  getNonUserToken(): Observable<any> {
    this.http = this.injector.get(HttpClient);
    const url = `${$config.AUTH_URL}getNonUserToken`;
    return this.http.post(url, { domainName: location.hostname }).pipe(
      map((data: any) => data),
      catchError((error: any) => throwError(error))
    );
  }

  getFromCart(): Observable<any> {
    this.http = this.injector.get(HttpClient);
    const url = `${$config.AUTH_URL}cart/get`;
    return this.http.get(url, { params: { domainName: location.hostname } }).pipe(
      map((data: any) => data),
      catchError((error: any) => throwError(error))
    );
  }

  joinAddresses(params: any): Observable<any> {
    this.http = this.injector.get(HttpClient);
    const url = `${$config.AUTH_URL}cart/joinAddresses`;
    return this.http.post(url, params, { headers: { "Content-Type": "application/x-www-form-urlencoded" } }).pipe(
      map((data: any) => data),
      catchError((error: any) => throwError(error))
    );
  }
}