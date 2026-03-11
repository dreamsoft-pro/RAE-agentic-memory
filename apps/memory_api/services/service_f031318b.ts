import api from '@/lib/api';

class TokenService {
    static async getNonUserToken(): Promise<any> {
        try {
            const response = await api.post(`${process.env.AUTH_URL}getNonUserToken`, {
                domainName: location.hostname,
            }, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            });

            return response.data;
        } catch (error) {
            throw new Error(JSON.stringify(error.response?.data || error.message));
        }
    }

    static async getFromCart(): Promise<any> {
        try {
            const $http = api; // Assuming 'api' is a service that provides http functionality
            const response = await $http.post(`${process.env.AUTH_URL}getFromCart`, {
                domainName: location.hostname,
            }, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                }
            });

            return response.data;
        } catch (error) {
            throw new Error(JSON.stringify(error.response?.data || error.message));
        }
    }
}

export default TokenService;

// Example usage in a Next.js component or route
import TokenService from './path/to/TokenService';

async function fetchTokens() {
    try {
        const token = await TokenService.getNonUserToken();
        console.log(token);
    } catch (error) {
        console.error(error.message);
    }
}