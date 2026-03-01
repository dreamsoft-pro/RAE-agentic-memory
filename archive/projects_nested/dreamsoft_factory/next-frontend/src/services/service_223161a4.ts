import api from '@/lib/api';

class AddressService {
    static async getAddresses(resource: string): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${resource}`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response?.data || new Error('Failed to fetch addresses');
        }
    }

    static async setForUser(addresses: any[]): Promise<any> {
        try {
            const resource = ['address', 'setAddressToUser'].join('/');
            const sendData = { addresses };
            const url = `${process.env.API_URL}/${resource}`;
            const response = await api.patch(url, sendData);
            return response.data;
        } catch (error) {
            throw error.response?.data || new Error('Failed to set user address');
        }
    }

    static async addAddress(data: any): Promise<any> {
        try {
            // Implementation for adding an address goes here
            const resource = 'address'; // Example resource, adjust as needed
            const url = `${process.env.API_URL}/${resource}`;
            const response = await api.post(url, data);
            return response.data;
        } catch (error) {
            throw error.response?.data || new Error('Failed to add address');
        }
    }
}

export default AddressService;