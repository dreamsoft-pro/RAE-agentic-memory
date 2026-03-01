import { $http, $q } from './httpBridge';
/**
 * Service: PsTypeService
 * Integrated by RAE-Feniks v57.12
 */

import React from "react";
import { useCalculator } from "../Calculator/CalculatorContext";
import { useCart } from "../CartContext";

import { Injectable, Inject } from 'angular';
import { $q, $http, $config, Restangular, $cacheFactory } from 'dependencies';

@Injectable()
export class PsTypeService {
    private cache: any;

    constructor(
        @Inject('$q') private $q: ng.IQService,
        @Inject('$http') private $http: ng.IHttpService,
        @Inject('$config') private $config: any,
        @Inject(Restangular) private Restangular: Restangular,
        @Inject('$cacheFactory') private $cacheFactory: ng.ICacheFactoryService
    ) {
        this.cache = $cacheFactory('ps_types');
    }

    public getAll(groupID: string, force: boolean): ng.IPromise<any> {
        const def = this.$q.defer();

        if (this.cache.get('collection' + groupID) && !force) {
            def.resolve(this.cache.get('collection' + groupID));
        } else {
            this.Restangular.all('ps_groups/' + groupID + '/ps_types').getList().then((data: any) => {
                this.cache.put('collection' + groupID, data.plain()); // we don't return plain because we need the object for put
                def.resolve(data.plain());
            }, (data: any) => {
                def.reject(data);
            });
        }

        return def.promise;
    }

    public forView(groupUrl: string, force: boolean): ng.IPromise<any> {
        const def = this.$q.defer();

        if (this.cache.get('collection' + groupUrl) && !force) {
            def.resolve(this.cache.get('collection' + groupUrl));
        } else {
            this.Restangular.all('ps_groups/' + groupUrl + '/ps_types/forView').getList().then((data: any) => {
                this.cache.put('collection' + groupUrl, data.plain());
                def.resolve(data.plain());
            }, (data: any) => {
                def.reject(data);
            });
        }

        return def.promise;
    }

    public getTypesData(typesList: any): ng.IPromise<any> {
        const def = this.$q.defer();
        this.$http({
            method: 'PATCH',
            url: this.$config.API_URL + 'ps_types/getTypesData',
            data: { types: typesList }
        }).then((data: any) => {
            def.resolve(data);
        }, (data: any) => {
            def.reject(data);
        });

        return def.promise;
    }

    public search(text: string): ng.IPromise<any> {
        const def = this.$q.defer();
        this.$http({
            method: 'GET',
            url: this.$config.API_URL + 'ps_types/search/' + text
        }).then((data: any) => {
            def.resolve(data);
        }, (data: any) => {
            def.reject(data);
        });

        return def.promise;
    }

    public getOneByID(groupID: string, typeID: string): ng.IPromise<any> {
        const def = this.$q.defer();
        this.$http({
            method: 'GET',
            url: this.$config.API_URL + 'ps_groups/' + groupID + '/ps_types/oneByID/' + typeID
        }).then((data: any) => {
            def.resolve(data);
        }, (data: any) => {
            def.reject(data);
        });

        return def.promise;
    }

    public cacheRemove(groupID: string): void {
        this.cache.remove('collection' + groupID);
    }
}