import api from '@/lib/api';
import { NextApiRequest, NextApiResponse } from 'next';

class AuthService {
    static async getCartData(): Promise<any> {
        try {
            const response = await api.get('/cart/get', {
                params: {
                    domainName: location.hostname,
                },
            });
            return response.data;
        } catch (error) {
            throw new Error(error);
        }
    }

    static async sendSMData(data: any): Promise<any> {
        try {
            const response = await api.post('/sm/send', data); // Assuming there's a POST method for sending SM data
            return response.data;
        } catch (error) {
            throw new Error(error);
        }
    }
}

export default AuthService;