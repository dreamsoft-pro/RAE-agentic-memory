import { useEffect, useState } from 'react';
import api from '@/lib/api';

class ModuleService {
    private resource: string = 'modules';
    private cache: any; // Adjust type based on actual implementation details of $cacheFactory
    private getAllDef: Promise<void> | null = null;

    constructor() {
        this.cache = {}; // Placeholder for actual caching logic based on your requirements
    }

    public async getAll(force?: boolean): Promise<any[]> {
        if (this.getAllDef === null || force || (await this.getAllDef).status === 1) {
            this.getAllDef = this.fetchAllData();
        }
        return await this.getAllDef;
    }

    private async fetchAllData(): Promise<any> {
        try {
            const response = await api.get(this.resource);
            // Cache logic here
            if (this.cache[this.resource]) {
                this.cache[this.resource] = response.data; // Example cache update
            }
            return { data: response.data, status: 1 };
        } catch (error) {
            console.error('Error fetching all modules:', error);
            return { data: [], status: -1 };
        }
    }
}

export default ModuleService;