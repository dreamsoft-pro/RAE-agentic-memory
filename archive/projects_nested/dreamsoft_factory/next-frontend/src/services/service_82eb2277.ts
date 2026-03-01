import api from '@/lib/api';

class CategoryDescriptionsService {

    private resource: string;
    private apiUrl: string;

    constructor(resource: string) {
        this.resource = resource;
        this.apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
    }

    async patchResource(data: any): Promise<any> {
        try {
            const response = await api.patch(`${this.apiUrl}/${this.resource}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Unknown error');
        }
    }

    getUploadUrl(): string {
        return `${this.apiUrl}/${this.resource}/files`;
    }

    async getFiles(): Promise<any> {
        try {
            const response = await api.get(`${this.apiUrl}/${this.resource}/files`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Unknown error');
        }
    }
}

export default CategoryDescriptionsService;