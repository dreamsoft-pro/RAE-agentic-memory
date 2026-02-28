import { useEffect, useState } from 'react';
import api from '@/lib/api';

export default class MarginsService {

    static async getAllSuppliers(): Promise<any> {
        try {
            const resource = ['margins_supplier', 'getAllSuppliers'].join("/");
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            console.error("Error fetching all suppliers:", error);
            throw error; // Rethrow to handle the error in calling code
        }
    }

    static async getSupplierMargins(): Promise<any> {
        try {
            const resource = 'margins_supplier';
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            console.error("Error fetching supplier margins:", error);
            throw error; // Rethrow to handle the error in calling code
        }
    }

    static async addSupplierMargins(data: any): Promise<any> {
        try {
            const resource = 'margins_supplier';
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
            const response = await api.post(url, data);
            return response.data;
        } catch (error) {
            console.error("Error adding supplier margins:", error);
            throw error; // Rethrow to handle the error in calling code
        }
    }
}