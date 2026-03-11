import api from '@/lib/api';

export default class CountService {
    async patchCartRestorePrices(resource: string, data: any): Promise<any> {
        try {
            const response = await api.patch($config.API_URL + [resource, 'cartRestorePrices'].join('/'), data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }
}