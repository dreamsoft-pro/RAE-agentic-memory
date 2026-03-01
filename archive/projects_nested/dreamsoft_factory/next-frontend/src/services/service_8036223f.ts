import api from '@/lib/api';

class DiscountService {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async removeGroup(id: number): Promise<void> {
        try {
            const response = await api.delete(`${this.resource}/discountGroups/${id}`);
            if (response.data.response) {
                console.log(response.data.message);
            } else {
                throw new Error('Failed to delete group');
            }
        } catch (error) {
            console.error(error);
            throw error;
        }
    }

    async getGroups(): Promise<any[]> {
        try {
            const response = await api.get(`${this.resource}/discountGroups`);
            return response.data;
        } catch (error) {
            console.error(error);
            throw error;
        }
    }
}

export default DiscountService;