import api from '@/lib/api';

class LangSettingsService {
    static async update(lang: any, resource: string): Promise<any> {
        try {
            const response = await api.post(`${process.env.API_URL}/${resource}`, lang);
            if (response.data.ID) {
                // Assuming cache.remove is a method you have and process.env.API_URL is your environment variable
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }
}