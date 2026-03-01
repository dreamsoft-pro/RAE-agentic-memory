import api from '@/lib/api';

class UserService {
    static async getRoles(user: any, resource: string, items: any[]): Promise<any> {
        const url = `${process.env.API_URL}/${[resource, user.ID, 'userRoles'].join('/')}`;
        
        try {
            const response = await api.post(url, items);
            if (response.data.response) {
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error('Response data is invalid.');
            }
        } catch (error) {
            throw error;
        }
    }

    static async getGroups(user: any): Promise<any> {
        const url = `${process.env.API_URL}/users/${user.ID}/groups`;
        
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default UserService;