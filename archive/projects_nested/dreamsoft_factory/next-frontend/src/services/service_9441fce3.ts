import api from '@/lib/api';

class TemplateVariablesService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async updateAssoc(id: number | string, data: any): Promise<any> {
        try {
            const response = await api.put(`${this.resource}/assoc/${id}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async remove(id: number | string): Promise<void> {
        try {
            await api.delete(`${this.resource}/${id}`);
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

// Usage example:
const service = new TemplateVariablesService('yourResourceName');
service.updateAssoc(123, { key: 'value' }).then(response => console.log(response)).catch(error => console.error(error));
service.remove(456).then(() => console.log('Removed successfully')).catch(error => console.error(error));