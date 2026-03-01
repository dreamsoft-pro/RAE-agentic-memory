/**
 * Service: SubCategoryDescriptionService
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
export class SubCategoryDescriptionService {
  private API_URL = 'your-api-url'; // Replace with your actual API URL

  constructor(private http: HttpClient) {}

  getAll(subcategoryURL: string): Observable<any> {
    return this.http.get(`${this.API_URL}subcategoriesDescriptions/subcategoriesDescriptionsPublic?categoryURL=${subcategoryURL}`).pipe(
      map((data: any) => data),
      catchError((error: any) => of(error))
    );
  }
}
