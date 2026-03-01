import api from '@/lib/api';

class TemplateService {
    private resource: string = 'local_templates';

    public async getAll(): Promise<any> {
        try {
            const response = await api.get(this.resource);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
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

export default TemplateService;