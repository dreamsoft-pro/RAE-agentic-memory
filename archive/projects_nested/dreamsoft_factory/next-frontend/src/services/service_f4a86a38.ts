import api from '@/lib/api';

class UserService {
    static async getRoles(user: { ID: string }, resource: string): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${[resource, user.ID, 'userRoles'].join('/')}`;
            const response = await api.get(url);
            
            if (response.data.response) {
                cache.remove('collection');
                return response.data.items;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    static async setRoles(user: { ID: string }, items: any[]): Promise<void> {
        try {
            const url = `${process.env.API_URL}/${[user.ID, 'userRoles'].join('/')}`;
            await api.put(url, items);
        } catch (error) {
            throw error;
        }
    }
}