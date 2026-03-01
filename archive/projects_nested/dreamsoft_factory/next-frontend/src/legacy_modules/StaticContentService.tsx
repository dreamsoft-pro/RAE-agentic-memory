/**
 * Service: StaticContentService
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
export class StaticContentService {
  private resource = ['dp_static_contents'];

  constructor(private http: HttpClient, private config: ConfigService) {}

  getResource(): string[] {
    return this.resource;
  }

  getContent(key: string): Observable<any> {
    const url = `${this.config.API_URL}/${this.getResource().join('/')}/getContent/${key}`;
    return this.http.get(url).pipe(
      map((data) => data),
      catchError((error: HttpErrorResponse) => {
        console.log(error);
        return throwError('An error occurred while fetching content.');
      })
    );
  }
}

This code has been modernized from AngularJS to Angular using TypeScript and RxJS, with a focus on converting the service to use Angular's HttpClient module for making HTTP requests. The `ConfigService` is assumed to be provided in a similar manner as `$config` was in the original AngularJS code. Adjustments might be needed based on your actual configuration setup.