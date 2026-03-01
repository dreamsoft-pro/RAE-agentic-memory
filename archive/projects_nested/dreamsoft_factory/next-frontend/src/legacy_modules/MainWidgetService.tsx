/**
 * Service: MainWidgetService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

/**
 */

import { Injectable, NgModule } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, defer, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import * as _ from 'lodash';

@Injectable({
  providedIn: 'root'
})
export class MainWidgetService {
  constructor(private httpClient: HttpClient) {}

  getMegaMenu(): Observable<any> {
    return this.dpCategoryService.getCategoryTree().pipe(
      map((categories) => {
        if (_.size(categories) > 0) {
          return categories;
        } else {
          throw new Error('No categories found');
        }
      }),
      catchError(() => of(false))
    );
  }

  getCreditLimit(): Observable<any> {
    return this.paymentService.getCreditLimit().pipe(
      map((data) => data),
      catchError(() => of(null))
    );
  }

  getSkinName(): Observable<string> {
    const setting = new SettingService('general');
    return defer(() => setting.getSkinName()).pipe(
      map((response: any) => response.skinName),
      catchError(() => of('default'))
    );
  }

  getForms(): Observable<any> {
    const setting = new SettingService('forms');
    return defer(() => setting.getPublicSettings()).pipe(
      map((response: any) => response),
      catchError(() => of([]))
    );
  }

  formatSizeUnits(bytes: number): string {
    // Implementation here
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return 'n/a';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(2)} ${sizes[i]}`;
  }
}