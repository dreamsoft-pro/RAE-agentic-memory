import api from '@/lib/api';

class DiscountService {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async updateDiscountGroup(data: any): Promise<any> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/discountGroups`;
        
        try {
            const response = await api.put(url, data);
            return response.data.response ? response.data : Promise.reject(response.data);
        } catch (error) {
            return Promise.reject(error);
        }
    }
}

export default DiscountService;