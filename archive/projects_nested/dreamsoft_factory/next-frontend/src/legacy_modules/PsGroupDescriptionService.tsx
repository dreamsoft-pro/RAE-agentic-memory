/**
 * Service: PsGroupDescriptionService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class PsGroupDescriptionService {
  private apiUrl = '/api/ps_groupDescriptions/groupDescriptionsPublic?groupUrl=';

  constructor(private http: HttpClient) {}

  getAll(groupUrl: string): Observable<any> {
    return this.http.get(`${this.apiUrl}${groupUrl}`).pipe(
      map((response: any) => response),
      catchError(error => of(error))
    );
  }
}
