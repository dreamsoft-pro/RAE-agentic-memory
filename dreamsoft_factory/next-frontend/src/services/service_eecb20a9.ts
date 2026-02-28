import api from '@/lib/api';

class TemplateVariablesService {
    private resource: string;
    
    constructor(resource: string) {
        this.resource = resource;
    }

    async getTemplates(): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/getTemplates`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    async getSelectors(): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/getSelectors`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    async getGlobalVariables(): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/getGlobalVariables`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default TemplateVariablesService;