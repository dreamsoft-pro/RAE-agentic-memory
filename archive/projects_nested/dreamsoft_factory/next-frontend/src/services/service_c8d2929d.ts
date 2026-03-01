import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class DpOrderService {
    private apiUrl: string;

    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }

    changeAddresses(orderID: number, params: any): Promise<any> {
        return axios.patch(`${this.apiUrl}/${resource}/changeAddresses/${orderID}`, params)
            .then(response => response.data)
            .catch(error => {
                throw error.response ? error.response.data : error.message;
            });
    }

    getMyZoneOffers(params?: any): Promise<any> {
        if (!params) {
            params = {};
        }
        return axios.get(`${this.apiUrl}/${resource}/myZoneOffers`, { params })
            .then(response => response.data)
            .catch(error => {
                throw error.response ? error.response.data : error.message;
            });
    }

    acceptOffer(data: any): Promise<any> {
        // Implement the logic for accepting an offer
        return axios.post(`${this.apiUrl}/${resource}/acceptOffer`, data)
            .then(response => response.data)
            .catch(error => {
                throw error.response ? error.response.data : error.message;
            });
    }
}

export default DpOrderService;