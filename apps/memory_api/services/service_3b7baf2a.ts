import api from '@/lib/api';
import { Module } from '@/types'; // Assuming you have this type defined somewhere

export default class ModuleService {
    async update(module: Module): Promise<any> {
        try {
            const response = await api.put(`${process.env.NEXT_PUBLIC_API_URL}/${resource}`, module);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error; // This will be handled by the caller
        }
    }

    async remove(id: string): Promise<any> {
        try {
            const response = await api.delete(`${process.env.NEXT_PUBLIC_API_URL}/${resource}/${id}`);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error; // This will be handled by the caller
        }
    }

    constructor() {
        this.checkResource();
    }

    private checkResource(): void {
        if (!resource) {
            throw new Error('Resource is not defined');
        }
    }
}