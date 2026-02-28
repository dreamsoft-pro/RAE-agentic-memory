import axios from 'axios';
import { Cache } from './cache'; // Adjust the import according to your cache implementation

class ComplexService {

    private API_URL: string;
    private cache: Cache;

    constructor(API_URL: string, cache: Cache) {
        this.API_URL = API_URL;
        this.cache = cache;
    }

    deleteResourceById(resource: string, id: number): Promise<any> {
        return new Promise((resolve, reject) => {
            axios.delete(`${this.API_URL}/${resource}/${id}`)
                .then(response => {
                    const data = response.data;
                    if (data.response) {
                        this.cache.remove(resource);
                        resolve(data);
                    } else {
                        reject(data);
                    }
                })
                .catch(error => {
                    reject(error.response ? error.response.data : error.message);
                });
        });
    }

    addGroup(complexID: number, name: string): Promise<any> {
        return new Promise((resolve, reject) => {
            const resource = this.getResource();
            axios.post(`${this.API_URL}/${resource}`, { complexID, name })
                .then(response => resolve(response.data))
                .catch(error => reject(error.response ? error.response.data : error.message));
        });
    }

    private getResource(): string {
        // Implement your logic to return the appropriate resource
        return 'your-resource-name';
    }
}