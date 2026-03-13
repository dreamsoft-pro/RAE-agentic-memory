import api from '@/lib/api';

class AuthService {
    static async cleanSession(): Promise<any> {
        const resource: string = 'cleanSession';
        const url: string = `${process.env.AUTH_URL}/${resource}`;
        
        try {
            const response = await api.get(url, {
                params: {
                    domainName: location.hostname
                },
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            });
            
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    static async updateDefaultAddress(param: any): Promise<any> {
        const resource: string = 'updateDefaultAddress'; // Assuming the endpoint name
        const url: string = `${process.env.AUTH_URL}/${resource}`;

        try {
            const response = await api.put(url, param, {
                headers: {
                    "Content-Type": "application/json"
                }
            });

            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }
}

export default AuthService;