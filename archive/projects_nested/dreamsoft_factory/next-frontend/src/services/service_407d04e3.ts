import api from '@/lib/api';

class UserService {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async changePass(data: any): Promise<any> {
        try {
            const response = await api.patch(this.resource + '/changePass', data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    async getCurrency(userID: string): Promise<any> {
        const url = `${process.env.API_URL}/${this.resource}/currency/${userID}`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default UserService;