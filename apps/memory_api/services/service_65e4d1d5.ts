import api from '@/lib/api';

class CartService {
    private resource: string;

    constructor() {
        this.resource = 'carts';
    }

    public async getAll(): Promise<any[]> {
        try {
            const response = await api.get(this.resource);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    public async update(id: string, data: any): Promise<any> {
        try {
            const response = await api.patch(`${this.resource}/${id}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    public async patch(id: string, data: any): Promise<any> {
        try {
            const response = await api.put(`${this.resource}/${id}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }
}

export default new CartService();