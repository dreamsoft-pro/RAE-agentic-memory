/**
 * Service: DomainService
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
import { LocalStorageService } from './localStorage.service'; // Assuming you have a similar service for localStorage
import { ConfigService } from './config.service'; // Assuming you have a similar service for $config

@Injectable({
  providedIn: 'root'
})
export class DomainService {
  private resource = 'domains';
  private cache: any;

  constructor(
    private http: HttpClient,
    private rootScope: RootScopeService,
    private localStorage: LocalStorageService,
    private config: ConfigService,
    private cacheFactory: $cacheFactory // Assuming this is how you import the cache factory
  ) {
    this.cache = this.cacheFactory(this.resource);
  }

  getAllDef: Observable<any> = null;

  public getAll(force: boolean = false): Observable<any> {
    if (_.isNull(this.getAllDef) || force || this.getAllDef.source$.getValue().status === 1) {
      this.getAllDef = defer(() => this.http.get(`${this.config.API_URL}${this.resource}`));
    }

    if (this.cache.get('collection') && !force) {
      return of(this.cache.get('collection'));
    } else {
      return this.getAllDef.pipe(
        map((data: any) => {
          this.cache.put('collection', data);
          return data;
        }),
        catchError((error: any) => {
          console.error('Error fetching domains:', error);
          throw error;
        })
      );
    }
  }

  public editDomain(domain: any): Observable<any> {
    const def = defer(() => this.http.put(`${this.config.API_URL}${this.resource}`, domain));

    return def.pipe(
      map((data: any) => {
        if (data.response) {
          this.cache.remove('collection');
          this.rootScope.$emit('Domain:editSuccess');
          return data;
        } else {
          throw new Error('Failed to edit domain');
        }
      }),
      catchError((error: any) => {
        console.error('Error editing domain:', error);
        throw error;
      })
    );
  }

  public getCurrentDomain(): Observable<any> {
    const def = defer(() => this.getAll());

    return def.pipe(
      map((data: any) => {
        const result = _.find(data, { selected: 1 });
        if (result) {
          this.localStorage.set('domainID', result.ID);
          this.rootScope.currentDomain = result;
          return result;
        } else {
          throw new Error('No domain found');
        }
      }),
      catchError((error: any) => {
        console.error('Error getting current domain:', error);
        throw error;
      })
    );
  }

  public getDomain(id: number): Observable<any> {
    const def = defer(() => this.getAll());

    return def.pipe(
      map((data: any) => {
        const domain = _.find(data, { ID: id });
        if (domain) {
          return domain;
        } else {
          throw new Error('Domain not found');
        }
      }),
      catchError((error: any) => {
        console.error('Error getting domain:', error);
        throw error;
      })
    );
  }

  public setDomain(id: number): void {
    this.getDomain(id).subscribe({
      next: (data) => {
        this.localStorage.set('domainID', id);
        this.rootScope.currentDomain = data;
      },
      error: (error) => console.error('Error setting domain:', error)
    });
  }
}

@NgModule({
  providers: [DomainService]
})
export class DomainModule {}