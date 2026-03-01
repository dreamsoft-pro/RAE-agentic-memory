import axios from 'axios';
import { API_URL } from './config'; // Assuming you have a config file with API_URL

export class DpAddressService {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    updateAddress(addressID: number, data: any): Promise<any> {
        return axios.patch(`${API_URL}/${this.resource}/updateAddress/${addressID}`, data)
            .then(response => response.data)
            .catch(error => Promise.reject(error));
    }

    getAddresses(type: string): Promise<any[]> {
        return axios.get(`${API_URL}/${this.resource}/getAddresses/${type}`)
            .then(response => response.data)
            .catch(error => Promise.reject(error));
    }

    addAddress(data: any, type: string): Promise<any> {
        return axios.post(`${API_URL}/${this.resource}/addAddress`, { data, type })
            .then(response => response.data)
            .catch(error => Promise.reject(error));
    }
}