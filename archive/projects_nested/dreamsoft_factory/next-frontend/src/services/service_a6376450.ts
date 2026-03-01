import api from '@/lib/api';

class UserService {
    private resource: string;
    private url: string;

    constructor(resource: string, configUrl: string) {
        this.resource = resource;
        this.url = `${configUrl}/${resource}`;
    }

    async editUser(user: any): Promise<any> {
        try {
            const response = await api.patch(this.url, user);
            if (response.response) {
                // Assuming cache is defined elsewhere in the project
                cache.remove('collection');
                return response;
            } else {
                throw new Error(JSON.stringify(response));
            }
        } catch (error) {
            throw error;
        }
    }
}