import api from '@/lib/api';
import { Cache } from '@/types'; // Assuming Cache is a type defined elsewhere

export default class IncreaseService {
    private resource: string;
    private cache: Cache;

    constructor(resource: string, cache: Cache) {
        this.resource = resource;
        this.cache = cache;
    }

    async fetch(force?: boolean): Promise<any> {
        if (this.cache.get(this.resource) && !force) {
            return this.cache.get(this.resource);
        } else {
            try {
                const response = await api.get(`/api/${this.resource}`);
                const data = response.data.plain();
                this.cache.put(this.resource, data);
                return data;
            } catch (error: any) {
                throw error;
            }
        }
    }

    async save(item: any): Promise<any> {
        try {
            const response = await api.patch(`/api/${this.resource}`, item);
            if (response.data.response) {
                this.cache.remove(this.resource);
                return response.data;
            } else {
                throw new Error('Save failed');
            }
        } catch (error: any) {
            throw error;
        }
    }
}