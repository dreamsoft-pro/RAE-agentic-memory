import api from '@/lib/api';
import { useEffect, useState } from 'react';

class CartService {
    static async patchCart(id: string, data: any): Promise<any> {
        try {
            const response = await api.patch(`carts/${id}`, data);
            if (response.response) {
                return response.plain();
            } else {
                throw new Error('Failed to patch cart');
            }
        } catch (error) {
            throw error;
        }
    }

    static async getMessages(cartID: string): Promise<any> {
        const resource = 'carts'; // Define the resource variable
        const url = `${api.baseURL}/${resource}/${cartID}/cart_messages`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    static async addMessage(cartID: string, message: any): Promise<any> {
        const resource = 'carts'; // Define the resource variable
        const url = `${api.baseURL}/${resource}/${cartID}/messages`;
        try {
            const response = await api.post(url, message);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}