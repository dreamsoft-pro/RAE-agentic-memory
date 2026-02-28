import api from '@/lib/api';

export default class TokenService {
    static async getCart() {
        const url = `${process.env.AUTH_URL}/cart/get`;
        try {
            const response = await api.get(url, {
                params: { domainName: location.hostname },
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            });
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    static joinAddresses(params: any): Promise<any> {
        const apiInstance = api; // Assuming $injector.get("$http") is similar to getting an instance of the API service
        return new Promise((resolve, reject) => {
            apiInstance.post('/some/address/endpoint', params)
                .then(response => resolve(response.data))
                .catch(error => reject(error.response ? error.response : error));
        });
    }
}