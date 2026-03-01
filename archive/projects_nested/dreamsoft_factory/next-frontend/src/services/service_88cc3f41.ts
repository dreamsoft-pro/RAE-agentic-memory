import axios from 'axios';
import { Cache } from './cache'; // Assuming you have a cache implementation

class ComplexService {
    private apiUrl: string;
    private cache: Cache;

    constructor(apiUrl: string, cache: Cache) {
        this.apiUrl = apiUrl;
        this.cache = cache;
    }

    public update(resource: string, item: any): Promise<any> {
        return new Promise((resolve, reject) => {
            axios.put(`${this.apiUrl}${resource}`, item)
                .then(response => {
                    if (response.data.response) {
                        this.cache.remove(resource);
                        resolve(response.data);
                    } else {
                        reject(response.data);
                    }
                })
                .catch(error => {
                    reject(error.response ? error.response.data : error.message);
                });
        });
    }

    public remove(id: string): Promise<any> {
        const resource = this.getResource();
        return new Promise((resolve, reject) => {
            axios.delete(`${this.apiUrl}${resource}/${id}`)
                .then(response => {
                    resolve(response.data);
                })
                .catch(error => {
                    reject(error.response ? error.response.data : error.message);
                });
        });
    }

    private getResource(): string {
        // Implement your logic to get the resource
        return ''; // Placeholder for actual implementation
    }
}