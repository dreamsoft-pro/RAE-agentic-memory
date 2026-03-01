import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class DpOrderService {
    private apiUrl: string;

    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }

    getMyZoneCount(params?: Record<string, any>): Promise<any> {
        return axios.get(`${this.apiUrl}/${resource}/myZoneCount`, { params })
            .then(response => response.data)
            .catch(error => {
                throw error.response ? error.response.data : error.message;
            });
    }

    sendPaymentSuccess(data: any, orderID: string): Promise<any> {
        return axios.patch(`${this.apiUrl}/${resource}/paymentSuccess/${orderID}`, data)
            .then(response => response.data)
            .catch(error => {
                throw error.response ? error.response.data : error.message;
            });
    }
}