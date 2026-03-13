/**
 * Service: PaymentService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class PaymentService {
  private apiUrl = '/api'; // Assuming you have a base API URL defined somewhere

  constructor(private http: HttpClient) {}

  getResource(): string[] {
    return ['payments', 'paymentsPublic'];
  }

  getAll(orderID: string): Observable<any> {
    const resource = this.getResource().concat(orderID ? [orderID] : []);
    return this.http.get(`${this.apiUrl}/${resource.join('/')}`).pipe(
      map((data: any) => data),
      catchError(this.handleError)
    );
  }

  getCreditLimit(): Observable<any> {
    const resource = ['payments', 'creditLimit'];
    return this.http.get(`${this.apiUrl}/${resource.join('/')}`).pipe(
      map((data: any) => data),
      catchError(this.handleError)
    );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    console.error('An error occurred:', error);
    return throwError('Something bad happened; please try again later.');
  }
}

This modernized code uses Angular's `HttpClient` for making HTTP requests, and it follows a more TypeScript-friendly structure with proper type definitions and error handling. The service is also marked as injectable using the `@Injectable` decorator.