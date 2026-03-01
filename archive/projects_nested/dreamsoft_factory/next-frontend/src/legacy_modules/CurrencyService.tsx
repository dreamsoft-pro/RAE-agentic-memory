/**
 * Service: CurrencyService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable, NgModule } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, defer, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { RootScopeService } from './rootScope.service'; // Assuming you have a RootScopeService

@Injectable({
  providedIn: 'root'
})
export class CurrencyService {
  private resource = 'currency';
  private cache = $cacheFactory(this.resource);
  private getAllDef: Observable<any> | null = null;

  constructor(private http: HttpClient, private rootScope: RootScopeService, private config: ConfigService) {}

  public getAll(force: boolean = false): Observable<any> {
    if (!this.getAllDef || force || this.getAllDef.pipe().isCompleted) {
      this.getAllDef = defer(() => this.http.get(`${this.config.API_URL}/${this.resource}`));
    }

    if (this.cache.get('collection') && !force) {
      return of(this.cache.get('collection'));
    } else {
      return this.getAllDef.pipe(
        map((data: any) => {
          this.cache.put('collection', data);
          this.rootScope.$emit('Currency.getAll', data);
          return data;
        }),
        catchError((error: any) => {
          console.error('Error fetching currencies:', error);
          throw error;
        })
      );
    }
  }

  public create(lang: any): Observable<any> {
    return defer(() => this.http.post(`${this.config.API_URL}/${this.resource}`, lang)).pipe(
      map((data: any) => {
        if (data.ID) {
          this.cache.remove('collection');
          return data;
        } else {
          throw new Error('Creation failed');
        }
      }),
      catchError((error: any) => {
        console.error('Error creating currency:', error);
        throw error;
      })
    );
  }

  public update(lang: any): Observable<any> {
    return defer(() => this.http.put(`${this.config.API_URL}/${this.resource}`, lang)).pipe(
      map((data: any) => {
        if (data.response) {
          return data;
        } else {
          throw new Error('Update failed');
        }
      }),
      catchError((error: any) => {
        console.error('Error updating currency:', error);
        throw error;
      })
    );
  }

  public remove(id: string): Observable<any> {
    return defer(() => this.http.delete(`${this.config.API_URL}/${this.resource}/${id}`)).pipe(
      map((data: any) => {
        if (data.response) {
          return data;
        } else {
          throw new Error('Removal failed');
        }
      }),
      catchError((error: any) => {
        console.error('Error removing currency:', error);
        throw error;
      })
    );
  }
}

@NgModule({
  providers: [CurrencyService]
})
export class CurrencyModule {}