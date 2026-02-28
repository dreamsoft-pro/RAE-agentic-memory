import api from '@/lib/api';

class TemplateService {
    private resource: string = 'templates'; // Example resource name

    public async uploadFile(template: any): Promise<any> {
        const formData = new FormData();
        formData.append('templateFile', template.file);
        
        return await api.post(`${this.resource}/${template.ID}/upload`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    }

    public async setSource(data: any): Promise<any> {
        try {
            const response = await api.patch(`${this.resource}/setSource`, data);
            if (response.data.response) {
                return response;
            } else {
                throw new Error('Response failed validation');
            }
        } catch (error) {
            throw error;
        }
    }
}

export default TemplateService;