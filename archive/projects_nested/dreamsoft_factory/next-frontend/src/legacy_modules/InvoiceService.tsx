/**
 * Service: InvoiceService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from 'angular';
import { HttpClient, HttpResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class InvoiceService {
  private resource = 'dp_invoices';

  constructor(private http: HttpClient) {}

  getForUser(orderID: string): Observable<ArrayBuffer> {
    const url = `${this.resource}/getForUser/${orderID}`;
    return this.http.get(url, { responseType: 'arraybuffer' }).pipe(
      map((response: HttpResponse<ArrayBuffer>) => response),
      catchError(error => throwError('Error fetching invoice'))
    );
  }
}
