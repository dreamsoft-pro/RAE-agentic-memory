import api from '@/lib/api';

class CategoryDescriptionsService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async addDescription(showLang: string, data: any): Promise<any> {
        try {
            const response = await api.post(`${this.resource}?showLang=${showLang}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    async removeDescription(id: string): Promise<void> {
        try {
            await api.delete([this.resource, id].join('/'));
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    async editDescription(data: any): Promise<any> {
        var def = $q.defer(); // This line needs to be handled as '$q' is not defined in the context and is Angular specific. We will convert this using native Promises.

        try {
            const response = await api.put(`${this.resource}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    // Add more methods here if necessary
}

export default CategoryDescriptionsService;