import api from '@/lib/api';

export default class AddressService {
    private getResource(): string {
        // Implement this method based on your requirements
        return 'some-resource';
    }

    public async save(data: any): Promise<any> {
        const resource = this.getResource();
        try {
            const response = await api.post(`${process.env.API_URL}/${resource}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error(String(error));
        }
    }

    public saveAddressToSession(addressID: string): Promise<any> {
        const params = { addressID };
        return this.save(params).catch((error) => {
            console.error('Failed to save address:', error);
            // Handle the error as needed
            throw error;
        });
    }
}