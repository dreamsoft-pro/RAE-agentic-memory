import api from '@/lib/api';

class AuthService {
    static async addCart(params: any): Promise<any> {
        const url = process.env.AUTH_URL + 'cart/add';
        try {
            const response = await api.post(url, $.param(params), {
                params: { domainName: location.hostname },
                headers: { "Content-Type": "application/x-www-form-urlencoded" }
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || new Error('Unknown API error');
        }
    }

    static async getSessionCarts(): Promise<any> {
        const url = process.env.AUTH_URL + 'some/cart/path'; // Adjust this URL as necessary
        try {
            const response = await api.get(url, { params: { domainName: location.hostname } });
            return response.data;
        } catch (error) {
            throw error.response?.data || new Error('Unknown API error');
        }
    }
}

export default AuthService;

// Usage example:
// AuthService.addCart({ /* your cart data */ })
//   .then(data => console.log(data))
//   .catch(error => console.error(error));