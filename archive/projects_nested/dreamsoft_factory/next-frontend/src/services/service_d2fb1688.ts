import { useEffect, useState } from 'react';
import axios from '@/lib/api';

class PsConfigAttributeTypeService {
    private resource: string = '/api/config/attribute-types'; // Assuming this API endpoint

    constructor() {}

    public async fetchAttributes(): Promise<any[]> {
        try {
            const response = await axios.get(this.resource);
            return response.data;
        } catch (error) {
            console.error('Failed to fetch attributes', error);
            throw error; // Re-throw for handling in the caller
        }
    }

    public async createAttribute(attribute: any): Promise<any> {
        try {
            const response = await axios.post(this.resource, attribute);
            return response.data;
        } catch (error) {
            console.error('Failed to create attribute', error);
            throw error; // Re-throw for handling in the caller
        }
    }

    public async updateAttribute(id: string, updatedAttribute: any): Promise<any> {
        try {
            const response = await axios.put(`${this.resource}/${id}`, updatedAttribute);
            return response.data;
        } catch (error) {
            console.error('Failed to update attribute', error);
            throw error; // Re-throw for handling in the caller
        }
    }

    public async deleteAttribute(id: string): Promise<void> {
        try {
            await axios.delete(`${this.resource}/${id}`);
        } catch (error) {
            console.error('Failed to delete attribute', error);
            throw error; // Re-throw for handling in the caller
        }
    }
}

export default PsConfigAttributeTypeService;