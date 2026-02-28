import api from '@/lib/api';

class AddressService {
    private resource: string = 'addresses'; // Assume this is the endpoint for addresses

    constructor() {}

    public async fetchAddresses(): Promise<string[]> {
        try {
            const response = await api.get(this.resource);
            return response.data.map(address => address.id); // Example of mapping to ids
        } catch (error) {
            console.error('Failed to fetch addresses:', error.response ? error.response.data : error.message);
            throw new Error('Unable to fetch addresses.');
        }
    }

    public async validateAddress(id: string): Promise<boolean> {
        try {
            const response = await api.get(`${this.resource}/${id}`);
            return this.isAddressValid(response.data); // Assuming there's a method for validation
        } catch (error) {
            console.error('Failed to validate address:', error.response ? error.response.data : error.message);
            throw new Error(`Unable to validate address ${id}.`);
        }
    }

    private isAddressValid(address: any): boolean {
        // Define your validation rules here
        if (!address.street || !address.city) return false;
        return true; // Example of a simple validation logic
    }
}

export default AddressService;