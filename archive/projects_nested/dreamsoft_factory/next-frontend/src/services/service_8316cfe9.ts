import api from '@/lib/api';
import { Cache } from '@/types/Cache'; // Assuming Cache is a type or interface for caching

class PsConfigOption {
    private cache: Cache;
    private resource: string;

    constructor(cache: Cache) {
        this.cache = cache;
        this.resource = ''; // Initialize the resource property
    }

    async fetchResource(force?: boolean): Promise<any> {
        if (this.cache.get(this.resource) && !force) {
            return this.cache.get(this.resource);
        } else {
            try {
                const data = await api.get(`/api/${this.resource}`);
                const plain = data.plain(); // Assuming 'plain' method is available
                this.cache.put(this.resource, plain);
                return plain;
            } catch (error) {
                throw error;
            }
        }
    }

    async copy(optID: string): Promise<any> {
        try {
            const response = await api.get(`/api/${this.getResource()}/copy/${optID}`);
            if (response.response) {
                return response;
            } else {
                throw new Error('Copy operation failed');
            }
        } catch (error) {
            throw error;
        }
    }

    private getResource(): string {
        // Implement logic to get resource based on optID or any other condition
        return this.resource; // Example, replace with actual implementation
    }
}