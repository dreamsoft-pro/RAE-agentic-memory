import api from '@/lib/api';
import { useState } from 'react';

export default class DiscountService {
    private static resource: string = '/discounts';  // Define this appropriately based on your API requirements

    public static async create(data: any): Promise<any> {
        try {
            const response = await api.post(DiscountService.resource, data);
            if (response.data.response) {
                cache.remove('collection');  // Assuming cache is defined elsewhere
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;  // Re-throw the error for further handling downstream
        }
    }

    public static async update(data: any): Promise<any> {
        try {
            const response = await api.put(`${DiscountService.resource}/${data.id}`, data);  // Assuming API requires an ID in the URL
            if (response.data.response) {
                cache.remove('collection');  // Assuming cache is defined elsewhere
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;  // Re-throw the error for further handling downstream
        }
    }
}

// Example usage of DiscountService in a Next.js component
function MyComponent() {
    const [createdData, setCreatedData] = useState(null);
    const [updatedData, setUpdatedData] = useState(null);

    async function onCreate(data) {
        try {
            const response = await DiscountService.create(data);
            setCreatedData(response);
        } catch (error) {
            console.error('Error creating discount:', error);
        }
    }

    async function onUpdate(data) {
        try {
            const response = await DiscountService.update(data);
            setUpdatedData(response);
        } catch (error) {
            console.error('Error updating discount:', error);
        }
    }

    return (
        <div>
            {/* Render your component UI */}
        </div>
    );
}