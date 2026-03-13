/**
 * Service: DpProductService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'angular';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class DpProductService {
  private resource = 'dp_products';

  constructor(private httpClient: HttpClient, private config: Config) {}

  getAll(): Observable<any> {
    return this.httpClient.get(`${this.config.API_URL}${this.resource}`).pipe(
      map((data: any) => data),
      catchError((error: HttpErrorResponse) => throwError(error))
    );
  }

  baseInfo(id: number): Observable<any> {
    return this.httpClient.get(`${this.config.API_URL}${this.resource}/baseInfo/${id}`).pipe(
      map((data: any) => data),
      catchError((error: HttpErrorResponse) => throwError(error))
    );
  }

  delete(product: any): Observable<any> {
    return this.httpClient.delete(`${this.config.API_URL}${this.resource}/deletePublic/${product.productID}`).pipe(
      map((data: any) => data),
      catchError((error: HttpErrorResponse) => throwError(error))
    );
  }

  deleteFromMongo(product: any): Observable<any> {
    return this.httpClient.post(`${this.config.AUTH_URL}cart/delete`, product, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).pipe(
      map((data: any) => data),
      catchError((error: HttpErrorResponse) => throwError(error))
    );
  }

  getByOrder(orderID: number): Observable<any> {
    return this.httpClient.get(`${this.config.API_URL}${this.resource}/getByOrder/${orderID}`).pipe(
      map((data: any) => data),
      catchError((error: HttpErrorResponse) => throwError(error))
    );
  }

  restoreAccept(productID: number): Observable<any> {
    return this.httpClient.patch(`${this.config.API_URL}${this.resource}/restoreAccept/${productID}`, null).pipe(
      map((data: any) => data),
      catchError((error: HttpErrorResponse) => throwError(error))
    );
  }
}