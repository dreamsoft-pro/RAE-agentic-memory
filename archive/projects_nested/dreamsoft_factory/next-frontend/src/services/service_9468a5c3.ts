import { useEffect, useState } from 'react';
import axios from '@/lib/api'; // Assuming this is a custom wrapper around Axios

class DeviceService {
    private resource: string;
    private apiUrl: string;

    constructor(resource: string) {
        this.resource = resource;
        this.apiUrl = process.env.NEXT_PUBLIC_API_URL; // Example env variable, adjust as necessary
    }

    public async get(id: number): Promise<any> {
        try {
            const response = await axios.get(`${this.apiUrl}/${this.resource}/${id}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error(error);
        }
    }

    public async create(data: any): Promise<any> {
        try {
            const response = await axios.post(`${this.apiUrl}/${this.resource}`, data);
            if (response.data.ID) {
                // Assuming cache is a global object or imported from somewhere
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error(response.data.error || 'Failed to create device');
            }
        } catch (error) {
            throw error.response ? error.response : new Error(error);
        }
    }

    public static async getStatic(id: number, resource: string): Promise<any> {
        const instance = new DeviceService(resource);
        return await instance.get(id);
    }

    public static async createStatic(data: any, resource: string): Promise<any> {
        const instance = new DeviceService(resource);
        return await instance.create(data);
    }
}

// Example usage
(async () => {
    try {
        console.log(await DeviceService.getStatic(123, 'devices'));
        console.log(await DeviceService.createStatic({ name: 'New Device' }, 'devices'));
    } catch (error) {
        console.error(error);
    }
})();