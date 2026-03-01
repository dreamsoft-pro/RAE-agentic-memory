/**
 * Service: CommonService
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
export class CommonService {
  private API_URL = 'your-api-url-here'; // Replace with your actual API URL

  constructor(private httpClient: HttpClient) {}

  getAll(): Observable<any> {
    return this.httpClient.get(`${this.API_URL}dp_ModelIconsExtensions`).pipe(
      map((response: any) => response),
      catchError((error: HttpErrorResponse) => {
        console.error('Error fetching data:', error);
        return throwError('Something went wrong; please try again later.');
      })
    );
  }
}
