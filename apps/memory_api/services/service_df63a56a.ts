import api from '@/lib/api';

export default class OrderService {

    static async getOngoings(orderID: string): Promise<any> {
        const resource = 'ongoings'; // Ensure resource is defined before use
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/${orderID}/ongoings`;
        
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Failed to fetch ongoing data');
        }
    }

    static async files(orderID: string): Promise<any> {
        const resource = 'files'; // Ensure resource is defined before use
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/files/${orderID}`;
        
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Failed to fetch file data');
        }
    }

    static async patchOngoings(orderID: string, ongoingID: string, data: any): Promise<any> {
        const resource = 'ongoings'; // Ensure resource is defined before use
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/${orderID}/ongoings/${ongoingID}`;
        
        try {
            const response = await api.patch(url, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Failed to patch ongoing data');
        }
    }

}