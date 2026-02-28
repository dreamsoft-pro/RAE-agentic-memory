/**
 * Service: CartService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from '@angular/core';
import { Restangular } from 'restangular';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  private resource = 'carts';

  constructor(private restangular: Restangular, private http: HttpClient) {}

  getAll(): Observable<any> {
    return this.restangular.all('carts').getList().pipe(
      map((data: any) => data.plain())
    );
  }

  update(id: number, data: any): Observable<any> {
    return this.restangular.one('carts', id).doPOST(data).pipe(
      map((response: any) => {
        if (response && response.response) {
          return response.plain();
        } else {
          throw new Error('No response data');
        }
      }),
      catchError((error: any) => of(error))
    );
  }

  patch(id: number, data: any): Observable<any> {
    return this.restangular.one('carts', id).patch(data).pipe(
      map((response: any) => {
        if (response && response.response === true) {
          return response.plain();
        } else {
          throw new Error('No response data');
        }
      }),
      catchError((error: any) => of(error))
    );
  }

  messages(cartID: number): Observable<any> {
    const url = `${$config.API_URL}/${this.resource}/${cartID}/cart_messages`;
    return this.http.get(url).pipe(
      map((data: any) => data),
      catchError((error: any) => of(error))
    );
  }

  addMessage(cartID: number, message: string): Observable<any> {
    const url = `${$config.API_URL}/${this.resource}/${cartID}/cart_messages`;
    return this.http.patch(url, { content: message }).pipe(
      map((data: any) => {
        if (data && data.response) {
          return data.item;
        } else {
          throw new Error('No response data');
        }
      }),
      catchError((error: any) => of(error))
    );
  }

  stats(params: HttpParams): Observable<any> {
    const url = `${$config.API_URL}/${this.resource}/stats`;
    return this.http.get(url, { params }).pipe(
      map((data: any) => data),
      catchError((error: any) => of(error))
    );
  }
}
