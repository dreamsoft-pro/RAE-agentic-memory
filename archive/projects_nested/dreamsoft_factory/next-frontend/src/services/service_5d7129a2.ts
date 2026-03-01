import api from '@/lib/api';

export default class UserService {

    private static async addUser(resource: string, data: any): Promise<any> {
        try {
            const response = await api.post($config.API_URL + resource, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public static addSimple(data: any): Promise<any> {
        return UserService.addUser('users/userSimpleRegister', data);
    }
}