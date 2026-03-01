import api from '@/lib/api';

export class ProcessService {
    private static async getAll(cache: any, resource: string, force?: boolean): Promise<any> {
        if (cache.get('collection') && !force) {
            return cache.get('collection');
        } else {
            try {
                const response = await api.get($config.API_URL + resource);
                cache.put('collection', response.data);
                return response.data;
            } catch (error) {
                throw error;
            }
        }
    }

    public static async create(data: any): Promise<any> {
        try {
            const response = await api.post($config.API_URL + 'resourcePathHere', data); // You need to specify the resource path
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}