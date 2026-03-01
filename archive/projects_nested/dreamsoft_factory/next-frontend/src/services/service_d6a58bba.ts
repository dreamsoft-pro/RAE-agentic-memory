import axios, { AxiosPromise } from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class UserAddressService {
    private apiUrl: string;

    constructor() {
        this.apiUrl = process.env.API_URL as string; // Ensure API_URL is set in your environment variables
    }

    deleteResource(id: number): AxiosPromise<any> {
        return axios.delete(`${this.apiUrl}/${this.resource}/${id}`, { data: { ID: id } })
            .then(response => response.data)
            .catch(error => Promise.reject(error));
    }
}

export default UserAddressService;