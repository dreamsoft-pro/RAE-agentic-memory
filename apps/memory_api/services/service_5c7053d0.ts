import axios from 'axios';
import { Cache } from './Cache'; // Assuming you have a custom cache implementation

export class CacheService<T> {
    private collection: string;
    private cache: Cache;

    constructor(collection: string) {
        this.collection = collection;
        this.cache = new Cache(collection);
    }

    public async doRequest(defer: () => Promise<string>, options?: any, method?: string): Promise<T | never> {
        const url = typeof defer === 'string' ? defer : await defer();
        let data: T;

        if (!options?.cache || !this.cache.get(url)) {
            try {
                const response = await axios({
                    url,
                    method: options?.method || 'get',
                    headers: { // Add any necessary headers here
                        'Content-Type': 'application/json'
                    }
                });
                data = response.data as T;
                this.cache.put(url, data);
            } catch (error) {
                throw error.response ? error.response : error;
            }
        } else {
            data = this.cache.get(url) as T;
        }

        return data;
    }
}