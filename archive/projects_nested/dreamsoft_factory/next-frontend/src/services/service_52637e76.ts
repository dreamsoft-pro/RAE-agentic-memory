import api from '@/lib/api';
import { Cache } from 'your-cache-library'; // You need to replace this with your actual cache library import

class YourClass {
    private resource: string;
    private url: string; // Ensure you define these properties somewhere in your class or constructor
    private cache: Cache;

    constructor(resource: string, cache: Cache) {
        this.resource = resource;
        this.cache = cache;
    }

    public async fetchData(force?: boolean): Promise<any> {
        if (this.cache.get(this.resource) && !force) {
            return this.cache.get(this.resource);
        } else {
            try {
                const response = await api.get(`${this.url}/${this.resource}`);
                const data = response.data;
                this.cache.put(this.resource, data);
                return data;
            } catch (error) {
                throw error; // You can handle the error differently if needed
            }
        }
    }
}