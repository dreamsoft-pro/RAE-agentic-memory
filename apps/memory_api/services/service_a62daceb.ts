import axios from '@/lib/api';
import type { Address } from '@/types'; // Assuming some generic types are defined here

class AddressService {
    resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    static async getAddresses(): Promise<Address[]> {
        try {
            const response = await axios.get(`${process.env.AUTH_URL}/addresses`, {
                params: { domainName: location.hostname }
            });
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Unexpected error occurred');
        }
    }

    static async getDefaultAddress(): Promise<Address> {
        try {
            const url = `${process.env.API_URL}/${this.resource}/getDefault?type=1`;
            const response = await axios.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Unexpected error occurred');
        }
    }

    updateProductAddresses(orderID: string, productID: string, productAddresses: Address[]): Promise<void> {
        try {
            const url = `${process.env.API_URL}/${this.resource}/updateProductAddresses`;
            return axios.post(url, { orderID, productID, productAddresses });
        } catch (error) {
            throw error.response ? error.response : new Error('Unexpected error occurred');
        }
    }

    // Add more methods as needed
}