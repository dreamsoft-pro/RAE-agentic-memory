/**
 * Service: LangSettingsRootService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable, NgModule } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, defer, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { RootScopeService } from './rootScope.service'; // Assuming you have a similar service for $rootScope

@Injectable({
  providedIn: 'root'
})
export class LangSettingsRootService {
  private resource = 'langsettingsroot';
  private cache: any;

  constructor(private http: HttpClient, private rootScope: RootScopeService, private config: ConfigService) {
    this.cache = $cacheFactory(this.resource);
  }

  getAll(force?: boolean): Observable<any> {
    let getAllDef: any;

    if (_.isNull(getAllDef) || force || getAllDef.promise.$$state.status === 1) {
      getAllDef = defer(() => this.http.get(`${this.config.API_URL}${this.resource}`));
    } else {
      return of(getAllDef.promise);
    }

    if (this.cache.get('collection') && !force) {
      getAllDef.next(this.cache.get('collection'));
    } else {
      this.http.get(`${this.config.API_URL}${this.resource}`).pipe(
        map((data: any) => {
          this.cache.put('collection', data);
          this.rootScope.$emit('LangSettingsRoot.getAll', data);
          return of(data);
        }),
        catchError((error: any) => {
          getAllDef.next(null);
          return throwError(error);
        })
      ).subscribe();
    }

    return getAllDef;
  }

  create(lang: any): Observable<any> {
    return this.http.post(`${this.config.API_URL}${this.resource}`, lang).pipe(
      map((data: any) => {
        if (data.response) {
          this.cache.remove('collection');
          return of(data.item);
        } else {
          return throwError(data);
        }
      }),
      catchError((error: any) => {
        return throwError(error);
      })
    );
  }

  update(lang: any): Observable<any> {
    return this.http.put(`${this.config.API_URL}${this.resource}`, lang).pipe(
      map((data: any) => {
        if (data.response) {
          return of(data);
        } else {
          return throwError(data);
        }
      }),
      catchError((error: any) => {
        return throwError(error);
      })
    );
  }

  remove(id: string): Observable<any> {
    return this.http.delete(`${this.config.API_URL}${this.resource}/${id}`).pipe(
      map((data: any) => {
        if (data.response) {
          return of(data);
        } else {
          return throwError(data);
        }
      }),
      catchError((error: any) => {
        return throwError(error);
      })
    );
  }
}