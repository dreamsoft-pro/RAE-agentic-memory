import api from '@/lib/api';

class TemplateRootService {

    private resource: string = 'templates';

    public async getTemplateUrl(templateID: string): Promise<string> {
        try {
            const response = await api.get(`${this.resource}/getUrl/${templateID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

}

export default new TemplateRootService();