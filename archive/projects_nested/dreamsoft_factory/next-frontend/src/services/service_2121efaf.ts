import api from '@/lib/api';
import { Cache } from 'path-to-cache-module'; // Assume there is some caching mechanism in place

class OperationService {
    private cache: Cache; // Define cache instance
    private resource: string = ''; // Initialize resource variable

    constructor(cache: Cache, resource: string) {
        this.cache = cache;
        this.resource = resource;
    }

    async sort(operationId: number, sortData: any): Promise<any> {
        try {
            const response = await api.patch(`${this.resource}/${operationId}/sort`, sortData);
            if (response.data.response) {
                this.cache.remove('collection');
                return response.data;
            } else {
                throw new Error(response.data.message); // Or handle as per your error handling logic
            }
        } catch (error) {
            throw error; // Rethrow or log the error appropriately
        }
    }

    async devices(operationId: number): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/${operationId}/operationDevices`);
            return response.data;
        } catch (error) {
            throw error; // Handle or rethrow the error as needed
        }
    }
}

export default OperationService;