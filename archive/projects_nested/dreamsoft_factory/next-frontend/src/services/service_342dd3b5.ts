import api from '@/lib/api';

export default class CustomProductService {

    private resource: string = 'dp_customProducts';

    public getUploadUrl(customProductId: number): string {
        return `${api.API_URL}/${this.resource}/files/${customProductId}`;
    }

    public async add(data: any): Promise<any> {
        try {
            const response = await api.post(this.resource, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}