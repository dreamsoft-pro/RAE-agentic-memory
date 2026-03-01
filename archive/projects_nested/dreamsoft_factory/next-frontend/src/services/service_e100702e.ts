import api from '@/lib/api';

class TaxService {
    private static async update(lang: any): Promise<any> {
        try {
            const response = await api.put($config.API_URL + resource, lang);
            if (response.data.response) {
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error: any) {
            throw error;
        }
    }

    private static async create(lang: any): Promise<any> {
        try {
            const response = await api.post($config.API_URL + resource, lang);
            if (response.data.ID) {
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error: any) {
            throw error;
        }
    }

    // Example of how to use these methods
    static async performAction(lang: any, actionType: 'create' | 'update'): Promise<any> {
        if (actionType === 'create') {
            return TaxService.create(lang);
        } else if (actionType === 'update') {
            return TaxService.update(lang);
        }
        throw new Error('Invalid action type');
    }

}

export default TaxService;