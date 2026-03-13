import api from '@/lib/api';

class UserService {
    static async add(data: any, resource: string): Promise<any> {
        try {
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${[resource, 'special'].join('/')}`;
            const response = await api.post(url, data);
            if (response.data.response) {
                // Assuming cache is a global object or imported from somewhere
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