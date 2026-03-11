import api from '@/lib/api';

export default class AdminHelpService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async getModule(module: string): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/${module}/helpKeys`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    async create(data: any): Promise<any> {
        try {
            const response = await api.post(this.resource, data);
            if (response.data.response) {
                // Assuming cache is defined elsewhere and can be accessed
                cache.remove('collection');
                return response.data.item;
            } else {
                throw response.data;
            }
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    async update(module: string): Promise<any> {
        // Assuming the implementation of this method will be similar to create or getModule
        try {
            // Example endpoint modification based on module requirements, replace with actual API call
            const response = await api.put(`${this.resource}/${module}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }
}