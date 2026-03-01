/**
 * Service: TypePatternService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class TypePatternService {
  private resource = 'ps_patterns';
  private apiUrl = `${process.env.API_URL}`;

  constructor(private http: HttpClient) {}

  getUploadUrl(): string {
    return `${this.apiUrl}/${this.resource}/upload`;
  }

  getList(typeID: number, descID: number): Observable<any> {
    const params = new HttpParams().set('typeID', typeID.toString()).set('descID', descID.toString());
    return this.http.get(`${this.apiUrl}/${this.resource}/patternsPublic`, { params }).pipe(
      map((data: any) => data),
      catchError(error => of(error))
    );
  }
}
