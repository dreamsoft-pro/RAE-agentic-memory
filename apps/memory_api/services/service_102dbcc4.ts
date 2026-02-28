import api from '@/lib/api';

class CartService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async updateCartMessage(cartID: string, message: string): Promise<any> {
        try {
            const response = await api.patch(`${this.resource}/${cartID}/cart_messages`, { content: message });
            return response.data.response ? response.data.item : Promise.reject(response.data);
        } catch (error) {
            return Promise.reject(error);
        }
    }

    async stats(params?: any): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/stats`, { params });
            return response.data;
        } catch (error) {
            return Promise.reject(error);
        }
    }
}

export default CartService;