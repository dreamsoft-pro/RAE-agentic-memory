import api from '@/lib/api';

class DiscountService {
    private static async createGroup(data: any): Promise<any> {
        try {
            const response = await api.post(`${resource}/discountGroups`, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    private static async updateGroup(data: any): Promise<any> {
        try {
            const response = await api.put(`${resource}/discountGroups/${data.id}`, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    // Add other methods here as necessary

    public static async fetchGroup(groupId: string): Promise<any> {
        try {
            const response = await api.get(`${resource}/discountGroups/${groupId}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default DiscountService;