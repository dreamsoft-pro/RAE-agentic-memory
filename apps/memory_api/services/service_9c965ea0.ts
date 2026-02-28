import api from '@/lib/api';

class TemplateVariablesService {
    static async getGlobal(resource: string): Promise<any> {
        try {
            const response = await api.get(`${resource}/getGlobal`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    static async getForRange(range: string, id: number, resource: string): Promise<any> {
        try {
            const url = `${resource}/getForRange?range=${encodeURIComponent(range)}&id=${encodeURIComponent(id.toString())}`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    static async add(data: any): Promise<any> {
        try {
            const response = await api.post(resource, data); // Note: 'resource' should be defined before use
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }
}

// Example usage:
TemplateVariablesService.getGlobal('exampleResource')
    .then(data => console.log(data))
    .catch(error => console.error(error));

TemplateVariablesService.getForRange('2023-01', 456, 'anotherResource')
    .then(data => console.log(data))
    .catch(error => console.error(error));