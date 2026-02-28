/**
 * Service: PsComplexService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable, Inject } from 'angular';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, defer } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

@Injectable()
export class PsComplexService {
    private apiUrl: string;
    private cache = $cacheFactory('ps_complex');

    constructor(private http: HttpClient, @Inject('API_URL') private baseUrl: string) {
        this.apiUrl = `${baseUrl}/ps_groups/{groupID}/ps_types/{typeID}/ps_complex`;
    }

    getResource(): string {
        return `ps_groups/${this.groupID}/ps_types/${this.typeID}/ps_complex`;
    }

    getAll(): Observable<any> {
        const resource = this.getResource();
        return this.http.get(`${this.baseUrl}/${resource}`).pipe(
            map(data => data),
            catchError(error => this.handleError(error))
        );
    }

    getAllPublic(): Observable<any> {
        const resource = this.getResource();
        return this.http.get(`${this.baseUrl}/${resource}/complexPublic`).pipe(
            map(data => data),
            catchError(error => this.handleError(error))
        );
    }

    add(baseID: number, typeID: number, complexGroupID: number): Observable<any> {
        const resource = this.getResource();
        return this.http.post(`${this.baseUrl}/${resource}`, { baseID, typeID, complexGroupID }).pipe(
            map(data => data),
            catchError(error => this.handleError(error))
        );
    }

    addGroup(complexID: number, name: string): Observable<any> {
        const resource = this.getResource();
        return this.http.post(`${this.baseUrl}/${resource}/group/${complexID}`, { name }).pipe(
            map(data => data),
            catchError(error => this.handleError(error))
        );
    }

    editGroup(groupID: number, name: string): Observable<any> {
        const resource = this.getResource();
        return this.http.post(`${this.baseUrl}/${resource}`, { groupID, name }).pipe(
            map(data => data),
            catchError(error => this.handleError(error))
        );
    }

    edit(item: any): Observable<any> {
        const resource = this.getResource();
        return this.http.put(`${this.baseUrl}/${resource}`, item).pipe(
            map(data => data),
            catchError(error => this.handleError(error))
        );
    }

    remove(id: number): Observable<any> {
        const resource = this.getResource();
        return this.http.delete(`${this.baseUrl}/${resource}/${id}`).pipe(
            map(data => data),
            catchError(error => this.handleError(error))
        );
    }

    relatedFormat(baseFormatID: number): Observable<any> {
        const resource = this.getResource();
        return this.http.get(`${this.baseUrl}/${resource}/relatedFormat/${baseFormatID}`).pipe(
            map(data => data),
            catchError(error => this.handleError(error))
        );
    }

    saveRelatedFormat(baseFormatID: number, formats: any): Observable<any> {
        const resource = this.getResource();
        return this.http.post(`${this.baseUrl}/${resource}/relatedFormat/${baseFormatID}`, { formats }).pipe(
            map(data => data),
            catchError(error => this.handleError(error))
        );
    }

    private handleError(error: any): Observable<any> {
        console.error('An error occurred:', error);
        return defer(() => throwError(error));
    }
}