import api from '@/lib/api';

class GroupDescriptionsService {

    private resource: string;
    
    constructor(resource: string) {
        this.resource = resource;
    }

    public async updateDescription(data: any): Promise<any> {
        try {
            const response = await api.patch($config.API_URL + this.resource, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public getUploadUrl(): string {
        return $config.API_URL + [this.resource, 'files'].join('/');
    }

    public async getFiles(): Promise<any[]> {
        try {
            const response = await api.get($config.API_URL + [this.resource, 'files'].join('/'));
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

export default GroupDescriptionsService;