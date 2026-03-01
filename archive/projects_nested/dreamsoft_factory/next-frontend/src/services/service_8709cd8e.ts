import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class ReclamationService {
    static add(data: any, orderID: string): Promise<any> {
        return axios.post(`${process.env.API_URL}/${resource}/${orderID}`, data)
            .then(response => response.data)
            .catch(error => {
                throw error.response ? error.response : new Error('Request failed');
            });
    }

    static findByOrder(orderID: string): Promise<any> {
        return axios.get(`${process.env.API_URL}/${resource}/findByOrder/${orderID}`)
            .then(response => response.data)
            .catch(error => {
                throw error.response ? error.response : new Error('Request failed');
            });
    }

    static getAll(params?: any): Promise<any> {
        // Implementation for getAll method
        return axios.get(`${process.env.API_URL}/${resource}`, { params })
            .then(response => response.data)
            .catch(error => {
                throw error.response ? error.response : new Error('Request failed');
            });
    }
}