import api from '@/lib/api';

class SubcategoryDescriptionsService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async update(data: any): Promise<any> {
        try {
            const response = await api.put(`${$config.API_URL}${this.resource}`, data);
            return response.data;
        } catch (error) {
            throw error.response?.data || new Error('An unexpected error occurred');
        }
    }

    getDescription(data: any): Promise<any> {
        return this.request({ method: 'GET', url: `${$config.API_URL}${this.resource}`, data }).then(response => response.data);
    }

    async sort(data: any): Promise<void> {
        try {
            const response = await api.put(`${$config.API_URL}${this.resource}/sort`, data); // Adjust URL as needed
            return; // Return nothing or handle the response as needed
        } catch (error) {
            throw error.response?.data || new Error('An unexpected error occurred');
        }
    }

    private async request(config: { method: string, url: string, data?: any }): Promise<any> {
        try {
            const response = await api.request({
                ...config,
                baseURL: $config.API_URL
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || new Error('An unexpected error occurred');
        }
    }
}

// Example usage:
const service = new SubcategoryDescriptionsService('your-resource-path');
service.update({ /* your data */ }).then(data => console.log(data)).catch(err => console.error(err));