/**
 * Service: OrderMessagesService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class OrderMessageService {
  private resource = 'dp_orders_messages';
  private apiUrl = `${process.env.API_URL}`;

  constructor(private http: HttpClient) {}

  getMessages(orderID: string): Observable<any> {
    const url = `${this.apiUrl}/${this.resource}/myZone/${orderID}`;
    return this.http.get(url).pipe(
      map((data: any) => data),
      catchError((error: any) => of(error))
    );
  }

  countMessages(): Observable<any> {
    const url = `${this.apiUrl}/${this.resource}/countAll`;
    return this.http.get(url).pipe(
      map((data: any) => data),
      catchError((error: any) => of(error))
    );
  }
}
