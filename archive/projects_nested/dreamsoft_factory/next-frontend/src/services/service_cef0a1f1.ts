import api from '@/lib/api';

class SubcategoryDescriptionsService {

    private readonly resource: string;
    private readonly showLang: string;

    constructor(resource: string, showLang: string) {
        this.resource = resource;
        this.showLang = showLang;
    }

    public async postDescription(data: any): Promise<any> {
        try {
            const response = await api.post(`${this.resource}?showLang=${this.showLang}`, data);
            return response.data;
        } catch (error) {
            throw error.response?.data || new Error('Failed to fetch data');
        }
    }

    public async removeDescription(id: string): Promise<any> {
        try {
            const response = await api.delete(`${this.resource}/${id}`);
            return response.data;
        } catch (error) {
            throw error.response?.data || new Error(`Failed to delete description with id ${id}`);
        }
    }

    public async editDescription(data: any): Promise<any> {
        // Implement this method according to your specific requirements.
        // This is left as an exercise, since the original code snippet was cut off.
        return api.put(`${this.resource}/${data.id}`, data) // Assuming 'data' has an id property and other necessary fields
            .then(response => response.data)
            .catch(error => {
                throw error.response?.data || new Error('Failed to edit description');
            });
    }
}

export default SubcategoryDescriptionsService;