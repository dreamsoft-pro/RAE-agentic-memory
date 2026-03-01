import { useState, useEffect } from 'react';
import api from '@/lib/api';

class PsWorkspaceService {
    private cache: any; // Assuming there's some form of caching mechanism similar to Angular's $cacheFactory
    private rootScopeEmitter: (eventKey: string, data?: any) => void;

    constructor(cache: any, rootScopeEmitter: (eventKey: string, data?: any) => void) {
        this.cache = cache;
        this.rootScopeEmitter = rootScopeEmitter;
    }

    async update(item: any): Promise<any> {
        try {
            const response = await api.put('ps_workspaces', item);
            if (response.data.response) { // Assuming the API response structure
                let collection = this.cache.get('collection');
                const idx = collection.findIndex(ws => ws.ID === item.ID); // FindIndex equivalent in native JS
                if (idx > -1) {
                    collection[idx] = {...item}; // Angular copy equivalent
                }
                this.cache.put('collection', collection);
                this.rootScopeEmitter('ps_workspaces', collection);
                return Promise.resolve(collection);
            } else {
                throw new Error(JSON.stringify(response.data)); // Reject with error message
            }
        } catch (error) {
            console.error(error); // Log the error for debugging purposes
            return Promise.reject(error);
        }
    }

    remove(item: any): void {
        api.delete(`ps_workspaces/${item.ID}`)
            .then(() => {
                let collection = this.cache.get('collection');
                const idx = collection.findIndex(ws => ws.ID === item.ID); // FindIndex equivalent in native JS
                if (idx > -1) {
                    collection.splice(idx, 1);
                }
                this.cache.put('collection', collection);
                this.rootScopeEmitter('ps_workspaces', collection);
            })
            .catch(error => console.error(error)); // Log the error for debugging purposes
    }
}

export default PsWorkspaceService;