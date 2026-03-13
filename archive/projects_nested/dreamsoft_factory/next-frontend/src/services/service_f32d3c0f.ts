import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class UserAddressService {
    private apiUrl: string;
    private resource: string;

    constructor(apiUrl: string, resource: string) {
        this.apiUrl = apiUrl;
        this.resource = resource;
    }

    public async getAllAddressesVat(): Promise<any> {
        try {
            const response = await axios.get(`${this.apiUrl}/${this.resource}?type=2`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async createAddress(data: any): Promise<any> {
        try {
            const response = await axios.post(`${this.apiUrl}/${this.resource}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}