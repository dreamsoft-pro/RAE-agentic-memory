import api from '@/lib/api';
import { Cache } from 'some-cache-library'; // Assuming you have some caching library like localForage or similar

class StatusService {
    private cache: Cache;

    constructor() {
        this.cache = new Cache(); // Initialize your cache here
    }

    async deleteResource(resource: string, id: number): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${[resource, id].join("/")}`;
            const response = await api.delete(url);

            if (response.data.response) {
                this.cache.remove('collection');
                return response.data;
            } else {
                throw new Error(response.data);
            }
        } catch (error) {
            throw error;
        }
    }

    // Add other methods here as necessary
}

export default StatusService;