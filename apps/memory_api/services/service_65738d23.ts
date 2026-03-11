import api from '@/lib/api';

class AddressService {
    private static async addAddress(params: any): Promise<any> {
        const url = `${process.env.AUTH_URL}/addresses/add`; // Use environment variables for URLs.
        
        try {
            const response = await api.post(url, params, {
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                params: { domainName: location.hostname }
            });
            
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error; // Handle the errors accordingly.
        }
    }

    private static async getAddressesFromSession(): Promise<any> {
        const url = `${process.env.AUTH_URL}/addresses/session`; // Assuming there's an endpoint for session addresses.

        try {
            const response = await api.get(url, { params: { domainName: location.hostname } });
            
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error; // Handle the errors accordingly.
        }
    }

    static addAddressToSession(params: any): Promise<any> {
        return AddressService.addAddress(params);
    }

    static getAddressesFromSession(): Promise<any> {
        return AddressService.getAddressesFromSession();
    }
}

export default AddressService;