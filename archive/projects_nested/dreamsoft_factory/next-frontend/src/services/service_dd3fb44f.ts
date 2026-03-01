import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

interface AddressData {
  // Define the shape of your address data here based on your requirements
}

class DpAddressService {

    private apiUrl: string;
    private resource: string = 'dp_addresses';

    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }

    getDefaultAddress(type: string): Promise<any> {
        return axios.get(`${this.apiUrl}/${this.resource}/getAddress/${type}`)
            .then(response => response.data)
            .catch(error => Promise.reject(error));
    }

    editUserAddress(data: AddressData, addressID?: string): Promise<any> {
        if (addressID === undefined) {
            addressID = '';
        }
        
        // Assuming you want to send a POST request with the data
        return axios.post(`${this.apiUrl}/${this.resource}/${addressID}`, data)
            .then(response => response.data)
            .catch(error => Promise.reject(error));
    }

}

export default DpAddressService;