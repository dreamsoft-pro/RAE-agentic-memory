import api from '@/lib/api';
import { useState } from 'react';

class PsWorkspaceService {
    private cache: any; // Assuming this is an existing cache service

    constructor(cache) {
        this.cache = cache;
    }

    async add(item): Promise<any> {
        try {
            const response = await api.post('ps_workspaces', item);
            if (response.data.ID) {
                let collection = this.cache.get('collection') || [];
                collection.push(response.data);
                this.cache.put('collection', collection);
                // Assuming $rootScope is a global object in your context
                window.$rootScope.$emit('ps_workspaces', collection);
                return collection;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    async edit(item): Promise<any> {
        try {
            const response = await api.put(`ps_workspaces/${item.ID}`, item); // Assuming you have a unique identifier for editing
            let collection = this.cache.get('collection') || [];
            let index = collection.findIndex((workspace: any) => workspace.ID === item.ID);
            if (index !== -1) {
                collection[index] = response.data;
                this.cache.put('collection', collection);
                window.$rootScope.$emit('ps_workspaces', collection);
                return collection;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }
}

export default PsWorkspaceService;