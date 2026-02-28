import { Cache } from '@/lib/cache'; // Assuming you have a cache service
import api from '@/lib/api';

export default class ModuleService {
    private static async getAll(cache: Cache, resource: string, force?: boolean): Promise<any> {
        if (cache.get('collection') && !force) {
            return cache.get('collection');
        } else {
            try {
                const response = await api.get(`${process.env.API_URL}/${resource}`);
                cache.put('collection', response.data);
                // Assuming you have a way to emit events in your Next.js application
                this.emitEvent(response.data); 
                return response.data;
            } catch (error) {
                throw error; // You can handle the error as needed, here it just rethrows for simplicity.
            }
        }
    }

    private static emitEvent(data: any): void {
        console.log('Module.getAll', data); // Placeholder event emission logic
        // Replace with actual Next.js mechanism to broadcast events if necessary
    }

    public static async getExtended(type: string, func?: () => Promise<any>): Promise<any> {
        const def = { resolve: (value) => value, reject: (reason) => reason } as const; // Simulating defer without bluebird
        try {
            const result = await (func ? func() : ModuleService.getAll(cache, type));
            return result;
        } catch (error) {
            throw error;
        }
    }

    private static cache: Cache; // Ensure the cache is defined before use

    constructor() {
        this.cache = new Cache(); // Example of initializing cache, replace with actual implementation
    }
}