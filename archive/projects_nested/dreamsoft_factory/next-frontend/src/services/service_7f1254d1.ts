import api from '@/lib/api';

class SubcategoryDescriptionsService {
    private resource: string;
    private apiUrl: string;

    constructor(resource: string) {
        this.resource = resource;
        this.apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
    }

    async patchResource(data: any): Promise<any> {
        try {
            const response = await api.patch(this.getApiUrlWithResource(), data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    getUploadUrl(): string {
        return this.getApiUrlWithFiles();
    }

    async getFiles(): Promise<any[]> {
        try {
            const response = await api.get(this.getApiUrlWithFiles());
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    private getApiUrlWithResource(): string {
        return `${this.apiUrl}/${this.resource}`;
    }

    private getApiUrlWithFiles(): string {
        return `${this.apiUrl}/${this.resource}/files`;
    }
}

export default SubcategoryDescriptionsService;