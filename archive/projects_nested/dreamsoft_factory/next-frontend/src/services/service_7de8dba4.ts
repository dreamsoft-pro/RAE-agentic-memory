import api from '@/lib/api';

class DiscountService {
    static async getProcessDiscounts(ID: string): Promise<any> {
        const resource = 'discounts'; // Define the resource variable before use
        const url = `${api.API_URL}/${[resource, 'showProcessDiscounts', ID].join('/')}`;

        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Failed to fetch data');
        }
    }
}

export default DiscountService;