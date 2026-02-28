import api from '@/lib/api';

class TemplateVariablesService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async saveAssoc(data: any): Promise<any> {
        try {
            const response = await api.post(this.resource + '/assoc', data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response error');
            }
        } catch (error) {
            throw error;
        }
    }
}