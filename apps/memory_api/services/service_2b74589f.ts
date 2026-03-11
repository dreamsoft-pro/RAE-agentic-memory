import api from '@/lib/api';

class UserService {
    static async userRegister(data: any): Promise<any> {
        const response = await api.post(`${process.env.API_URL}/${data.resource}/${data.user.ID}/userGroups`, data.items);

        if (response.data.response) {
            // Assuming `cache.remove` and `def.resolve`/`def.reject` are to be implemented in a similar fashion
            cache.remove('collection');
            return response.data;
        } else {
            throw new Error(response.data);
        }
    }

    static async fetchUserGroups(resource: string, userId: number, items: any[]): Promise<any> {
        try {
            const response = await api.post(`${process.env.API_URL}/${resource}/${userId}/userGroups`, items);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    // If you need to use $q.defer() pattern, you could wrap the fetchUserGroups in a promise-returning function like this:
    static userRegisterWithDeferred(data: any): Promise<any> {
        return new Promise((resolve, reject) => {
            UserService.fetchUserGroups(data.resource, data.user.ID, data.items)
                .then(resolve)
                .catch(reject);
        });
    }
}

export default UserService;