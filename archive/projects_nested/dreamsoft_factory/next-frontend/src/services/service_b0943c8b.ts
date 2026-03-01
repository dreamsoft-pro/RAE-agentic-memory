import api from '@/lib/api';

class UserService {
    static async getGroups(user: any): Promise<any[]> {
        try {
            const response = await api.get(`${process.env.API_URL}/${resource}/${user.ID}/userGroups`);
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

    static setGroups(user: any, items: any[]): Promise<void> {
        return new Promise((resolve, reject) => {
            api.put(`${process.env.API_URL}/${resource}/${user.ID}/userGroups`, { items })
                .then(response => resolve())
                .catch(error => reject(error));
        });
    }
}