import api from '@/lib/api';

class UserService {
    static async getUserFtp(resource: string): Promise<any> {
        try {
            const response = await api.get(`${resource}/getUserFtpData`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    static async getLoggedUserData(resource: string): Promise<any> {
        try {
            const response = await api.get(`${resource}/getLoggedUserData`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}