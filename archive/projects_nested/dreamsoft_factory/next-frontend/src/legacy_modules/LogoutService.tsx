/**
 * Service: LogoutService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { RootScopeService } from './rootScope.service';
import { LocalStorageService } from './localStorage.service';
import { NotificationService } from './notification.service';
import { TokenService } from './token.service';
import { AuthDataService } from './auth-data.service';
import { AuthService } from './auth.service';
import { TranslateFilter } from './translate.filter';

@Injectable({
  providedIn: 'root'
})
export class LogoutService {
  constructor(
    private http: HttpClient,
    private rootScopeService: RootScopeService,
    private localStorageService: LocalStorageService,
    private notificationService: NotificationService,
    private tokenService: TokenService,
    private authDataService: AuthDataService,
    private authService: AuthService,
    private translateFilter: TranslateFilter
  ) {}

  destroyUserData(): boolean {
    delete this.rootScopeService.username;
    this.authDataService.deleteAccessToken();
    this.localStorageService.remove('user');
    return true;
  }

  logout(): Observable<boolean> {
    return of(this.destroyUserData());
  }

  init(): Observable<boolean> {
    const def = new Observable<boolean>(observer => {
      this.authDataService.logout();
      this.notificationService.info(this.translateFilter('you_are_loggedout'));
      this.tokenService.getNonUserToken().then(data => {
        this.authService.setAccessToken(data.token);
        observer.next(true);
        observer.complete();
      });
    });

    return def;
  }
}
