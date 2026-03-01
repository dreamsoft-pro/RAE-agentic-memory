import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class DpOrderService {

    private static API_URL: string;

    static async sendPaymentStatus(orderID: number, urlParams: Record<string, any>): Promise<any> {
        try {
            const response = await axios.get(`${this.API_URL}/paymentStatus/${orderID}`, { params: urlParams });
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    static async payment(data: any, orderID: number): Promise<any> {
        try {
            const response = await axios.patch(`${this.API_URL}/payment/${orderID}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    static setAPIUrl(url: string): void {
        this.API_URL = url;
    }
}

export default DpOrderService;