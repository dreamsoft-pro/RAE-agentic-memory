import api from '@/lib/api';
import { Connect } from 'path-to-connect'; // Adjust the import path according to your file structure

class ConnectOptionService {
    static async patchPrice(connect: Connect, params: any): Promise<any> {
        try {
            const response = await api.patch(`${resource}/${connect.ID}/price`, params);
            return response.data;
        } catch (error) {
            throw error.response ? error : new Error('Internal Server Error');
        }
    }

    static async getPrices(connect: Connect): Promise<any> {
        try {
            const response = await api.get(`${resource}/${connect.ID}/price`);
            return response.data;
        } catch (error) {
            throw error.response ? error : new Error('Internal Server Error');
        }
    }
}