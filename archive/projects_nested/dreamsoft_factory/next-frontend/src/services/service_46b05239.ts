import api from '@/lib/api';

class UserService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async getMyAccount(): Promise<any> {
        try {
            const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/getMyAccount`);
            return response.data.response ? response.data : Promise.reject(response.data);
        } catch (error) {
            return Promise.reject(error);
        }
    }

    async checkOneTimeUser(): Promise<any> {
        try {
            const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/checkOneTimeUser`);
            return response.data.response ? response.data : Promise.reject(response.data);
        } catch (error) {
            return Promise.reject(error);
        }
    }
}

export default UserService;