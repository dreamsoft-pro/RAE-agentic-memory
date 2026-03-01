import api from '@/lib/api';

class OrderMessageService {
    private resource: string = 'dp_orders_messages';

    public async getMessages(orderID: string): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/${orderID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    public async countMessages(): Promise<number> {
        try {
            const response = await api.get(this.resource);
            // Assuming the API returns a count of messages
            return response.data.count; // Adjust according to actual API response structure
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }
}

export default OrderMessageService;