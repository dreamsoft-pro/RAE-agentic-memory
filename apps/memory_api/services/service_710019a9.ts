import api from '@/lib/api';

class LangRootService {
    private apiUrl: string;
    private resource: string;

    constructor(apiUrl: string, resource: string) {
        this.apiUrl = apiUrl;
        this.resource = resource;
    }

    async get(id?: number): Promise<any> {
        try {
            const url = id ? `${this.resource}/${id}` : this.resource;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    }

    async remove(id: number): Promise<any> {
        try {
            const url = `${this.resource}/${id}`;
            const response = await api.delete(url);
            if (!response.data.response) {
                throw new Error('Unexpected response format');
            }
            return response.data;
        } catch (error) {
            throw error.response?.data || error;
        }
    }
}

export default LangRootService;