// AddressService.ts

import api from '@/lib/api';

export default class AddressService {
    private resource: string = 'addresses';
    
    // Fetch all addresses for a given user ID.
    public async fetchAddresses(userId: number): Promise<any[]> {
        const url = `/users/${userId}/${this.resource}`;
        
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            console.error(`Failed to fetch ${this.resource} for user ID ${userId}. Error:`, error.response?.data || error.message);
            throw new Error('Unable to retrieve addresses.');
        }
    }

    // Add a new address for the specified user.
    public async addAddress(userId: number, addressData: any): Promise<any> {
        const url = `/users/${userId}/${this.resource}`;

        try {
            const response = await api.post(url, addressData);
            return response.data;
        } catch (error) {
            console.error(`Failed to add ${this.resource} for user ID ${userId}. Error:`, error.response?.data || error.message);
            throw new Error('Unable to add a new address.');
        }
    }

    // Update an existing address.
    public async updateAddress(userId: number, addressId: string, updatedData: any): Promise<any> {
        const url = `/users/${userId}/${this.resource}/${addressId}`;

        try {
            const response = await api.put(url, updatedData);
            return response.data;
        } catch (error) {
            console.error(`Failed to update ${this.resource} with ID ${addressId}. Error:`, error.response?.data || error.message);
            throw new Error('Unable to update the address.');
        }
    }

    // Delete an existing address.
    public async deleteAddress(userId: number, addressId: string): Promise<void> {
        const url = `/users/${userId}/${this.resource}/${addressId}`;

        try {
            await api.delete(url);
        } catch (error) {
            console.error(`Failed to delete ${this.resource} with ID ${addressId}. Error:`, error.response?.data || error.message);
            throw new Error('Unable to delete the address.');
        }
    }

    // Method for testing purposes, not intended for production.
    public async testMethod(): Promise<string> {
        try {
            return "Success!";
        } catch (error) {
            console.error("Failed in test method. Error:", error);
            throw new Error('Test failed.');
        }
    }
}