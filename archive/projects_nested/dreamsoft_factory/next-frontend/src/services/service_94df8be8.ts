import api from '@/lib/api';
import { AxiosResponse } from 'axios';

class TemplateVariablesService {
    private resource: string = 'templateVariables';

    async getAll(): Promise<AxiosResponse> {
        try {
            const response = await api.get(this.resource);
            return response;
        } catch (error) {
            throw error.response ? error.response : new Error('Request failed');
        }
    }

    async getTemplates(): Promise<AxiosResponse> {
        try {
            const response = await api.get(`${this.resource}/templates`);
            return response;
        } catch (error) {
            throw error.response ? error.response : new Error('Request failed');
        }
    }
}

export default TemplateVariablesService;