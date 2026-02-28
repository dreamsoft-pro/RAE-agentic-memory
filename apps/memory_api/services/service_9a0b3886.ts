import api from '@/lib/api';
import { Cache } from 'your-cache-module'; // Assuming you have some cache module in place
import { useState, useEffect } from 'react';

class PsWorkspaceService {
    private cache: Cache;
    
    constructor() {
        this.cache = new Cache(); // Initialize your cache here
    }

    async remove(itemID: string): Promise<void> {
        try {
            const response = await api.delete(`ps_workspaces/${itemID}`);
            
            if (response.status === 200) { // Assuming success is status code 200 or similar
                let collection = this.cache.get('collection');
                
                const idx = collection.findIndex(item => item.ID === parseInt(itemID));
                if (idx > -1) {
                    collection.splice(idx, 1);
                }
                
                this.cache.put('collection', collection);

                // Assuming $rootScope.$emit is some kind of event emitter
                window.dispatchEvent(new CustomEvent('ps_workspaces', { detail: collection }));

            } else {
                throw new Error(JSON.stringify(response));
            }

        } catch (error) {
            console.error("Failed to remove workspace", error);
        }
    }

    async getByPrintType(printTypeID: string): Promise<void> {
        try {
            const response = await api.get(`ps_workspaces?printTypeID=${printTypeID}`);
            
            if (response.status === 200) { // Assuming success is status code 200
                this.cache.put('collection', response.data); // Assuming data property holds the collection

                // Again, assuming some kind of event emitter mechanism
                window.dispatchEvent(new CustomEvent('ps_workspaces', { detail: response.data }));

            } else {
                throw new Error(JSON.stringify(response));
            }
        } catch (error) {
            console.error("Failed to get workspaces by print type", error);
        }
    }
}

export default PsWorkspaceService;