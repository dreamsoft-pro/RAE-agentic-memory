import api from '@/lib/api';

export default class MarginsService {
    private apiUrl: string;

    constructor() {
        this.apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
    }

    async create(resource: string[], margin: any): Promise<any> {
        try {
            const url = `${this.apiUrl}/${resource.join('/')}`;
            const response = await api.post(url, margin);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to create resource: ${error.message}`);
        }
    }

    async edit(resource: string[], ID: number | string, margin: any): Promise<any> {
        try {
            const url = `${this.apiUrl}/${resource.join('/')}/${ID}`;
            const response = await api.put(url, margin);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to edit resource with ID ${ID}: ${error.message}`);
        }
    }

    async removeMargin(resource: string[], ID: number | string): Promise<any> {
        try {
            const url = `${this.apiUrl}/${resource.join('/')}/${ID}`;
            const response = await api.delete(url);
            return response.data;
        } catch (error) {
            throw new Error(`Failed to delete resource with ID ${ID}: ${error.message}`);
        }
    }
}