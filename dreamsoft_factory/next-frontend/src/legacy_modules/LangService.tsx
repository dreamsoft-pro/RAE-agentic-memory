import { $http, $q } from './httpBridge';
/**
 * Service: LangService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

To modernize the provided JavaScript file (`LangService.js`) to TypeScript (TSX), we need to make several adjustments, including converting the code to use ES6 syntax and leveraging TypeScript's type system. Below is the converted TypeScript version of the file:

import { Injectable } from 'angular';
import { $q } from 'angular-es6-promise'; // Assuming angular-es6-promise for deferred objects
import { CacheService } from './CacheService'; // Adjust the import path as necessary
import { ConfigService } from './ConfigService'; // Adjust the import path as necessary

@Injectable()
export class LangService {
    private cacheResolve: CacheService;
    private resource: string = 'lang';

    constructor(private $rootScope: any, private $http: any, private config: ConfigService) {
        this.cacheResolve = new CacheService('lang');
    }

    public getAll(): ng.IPromise<any> {
        return this.cacheResolve.doRequest(this.resource).then((data: any) => {
            return data;
        }, (data: any) => {
            throw data;
        });
    }

    public getEmpty(): ng.IPromise<any> {
        return this.$q((resolve, reject) => {
            this.$http({
                method: 'GET',
                url: `${this.config.API_URL}/${this.resource}/showEmpty`
            }).then(function(data: any) {
                if (data.response) {
                    resolve(data);
                } else {
                    reject(data);
                }
            }, function(error: any) {
                reject(error);
            });
        });
    }

    public getLang(langCode: string): ng.IPromise<any> {
        return this.$q((resolve, reject) => {
            this.cacheResolve.doRequest(`${this.resource}/${langCode}`).then((data: any) => {
                if (data.response) {
                    resolve(data.response);
                } else {
                    reject(data);
                }
            }, function(data: any) {
                reject(data);
            });
        });
    }

    public edit(lang: any): ng.IPromise<any> {
        return this.$q((resolve, reject) => {
            this.$http({
                method: 'PUT',
                url: `${this.config.API_URL}/${this.resource}`,
                data: lang
            }).then(function(data: any) {
                if (data.response) {
                    resolve(data);
                } else {
                    reject(data);
                }
            }, function(error: any) {
                reject(error);
            });
        });
    }

    public remove(id: string): ng.IPromise<any> {
        return this.$q((resolve, reject) => {
            this.$http({
                method: 'DELETE',
                url: `${this.config.API_URL}/${this.resource}/${id}`
            }).then(function(data: any) {
                if (data.response) {
                    resolve(data);
                } else {
                    reject(data);
                }
            }, function(error: any) {
                reject(error);
            });
        });
    }
}

1. **TypeScript Syntax**: The code is now written in TypeScript, which includes type annotations for variables and method return types.
2. **ES6+ Features**: Utilizes modern JavaScript features like `import` statements for modules, arrow functions (`=>`), and template literals for string concatenation.
3. **Promises**: Uses `$q` from `angular-es6-promise` to handle asynchronous operations, which is a more TypeScript-friendly approach compared to the original jQuery-style callbacks.
4. **Injectable Decorator**: The Angular service is annotated with `@Injectable()` to indicate that it can be injected into other components.
5. **Type Annotations**: Added type annotations where necessary (`langCode`, `data`, etc.) and ensured method return types are properly defined.
6. **Error Handling**: Improved error handling by throwing errors directly from the promise chain using `reject`.

