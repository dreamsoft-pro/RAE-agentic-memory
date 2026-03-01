import { useEffect, useState } from 'react';
import axios from 'axios';
import lodash from 'lodash';

const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
const resource = 'domains';

export default class DomainService {
    private cache: Record<string, any>;
    private getAllDef: Promise<void> | null;

    constructor() {
        this.cache = {};
        this.getAllDef = null;
    }

    async getAll(force?: boolean): Promise<any[]> {
        if (lodash.isEqual(this.getAllDef, null) || force || (this.getAllDef && this.getAllDef.status === 1)) {
            this.getAllDef = axios.get(`${apiUrl}/${resource}`, { cache: false }).then(response => {
                this.cache[resource] = response.data;
                return Promise.resolve(response.data);
            }).catch(error => {
                console.error('Failed to fetch domains', error);
                return Promise.reject(error);
            });
        } else {
            return this.getAllDef.then((value) => value);
        }

        return [];
    }
}