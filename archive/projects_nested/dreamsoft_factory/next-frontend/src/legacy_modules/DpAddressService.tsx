/**
 * Service: DpAddressService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'angular';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, defer } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import _ from 'lodash';

@Injectable({
  providedIn: 'root'
})
export class DpAddressService {
  private resource = 'dp_addresses';
  private apiUrl = $config.API_URL;

  constructor(private http: HttpClient) {}

  getDefaultAddress(type: string): Observable<any> {
    const url = `${this.apiUrl}${this.resource}/getAddress/${type}`;
    return this.http.get(url).pipe(
      map((data: any) => data),
      catchError((error: any) => defer(() => Observable.throw(error)))
    );
  }

  editUserAddress(data: any, addressID?: string): Observable<any> {
    const url = `${this.apiUrl}${this.resource}/updateAddress/${addressID}`;
    return this.http.patch(url, data).pipe(
      map((response: any) => response),
      catchError((error: any) => defer(() => Observable.throw(error)))
    );
  }

  getAddresses(type: string): Observable<any> {
    const url = `${this.apiUrl}${this.resource}/getAddresses/${type}`;
    return this.http.get(url).pipe(
      map((data: any) => data),
      catchError((error: any) => defer(() => Observable.throw(error)))
    );
  }

  addAddress(data: any, type: string): Observable<any> {
    const url = `${this.apiUrl}${this.resource}/addAddress/${type}`;
    return this.http.post(url, data).pipe(
      map((response: any) => response),
      catchError((error: any) => defer(() => Observable.throw(error)))
    );
  }

  emptyAddress(): Observable<any> {
    const url = `${this.apiUrl}${this.resource}/emptyAddress`;
    return this.http.get(url).pipe(
      map((data: any) => data),
      catchError((error: any) => defer(() => Observable.throw(error)))
    );
  }

  remove(addressID: string): Observable<any> {
    const url = `${this.apiUrl}${this.resource}/${addressID}`;
    return this.http.delete(url).pipe(
      map((data: any) => data),
      catchError((error: any) => defer(() => Observable.throw(error)))
    );
  }
}