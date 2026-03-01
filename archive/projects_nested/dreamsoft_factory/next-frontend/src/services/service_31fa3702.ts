import axios from 'axios';
import { API_URL } from '../config'; // Adjust the import based on your project structure

class DpOrderService {
    static async getCart() {
        try {
            const response = await axios.get(API_URL + '/resource/getCart');
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    static async setUser(orderID: string) {
        try {
            const response = await axios.patch(`${API_URL}/resource/setUser/${orderID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    static async saveCart(orderID: string, sendData: any) {
        try {
            const response = await axios.put(`${API_URL}/resource/saveCart/${orderID}`, sendData);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }
}

export default DpOrderService;