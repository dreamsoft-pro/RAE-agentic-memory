import api from '@/lib/api';

class CurrencyRootService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async update(lang: any): Promise<any> {
        try {
            const response = await api.put(`${this.resource}`, lang);
            return response.data.response ? response : Promise.reject(response.data);
        } catch (error) {
            return Promise.reject(error.response?.data ?? error.message);
        }
    }

    async remove(id: string | number): Promise<any> {
        try {
            const response = await api.delete(`${this.resource}/${id}`);
            return response.data.response ? response : Promise.reject(response.data);
        } catch (error) {
            return Promise.reject(error.response?.data ?? error.message);
        }
    }
}

export default CurrencyRootService;