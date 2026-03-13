import api from '@/lib/api';

export default class PromotionService {
    private static resource: string;

    constructor(private readonly url: string, private readonly resource: string) {}

    public async create(data: any): Promise<any> {
        try {
            const response = await api.post(this.url + this.resource, data);
            if (response.data.response) {
                // Assuming cache.remove is an existing function for removing cache
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    public async update(data: any): Promise<any> {
        try {
            const response = await api.put(this.url + this.resource, data);
            if (response.data.response) {
                // Assuming cache.remove is an existing function for removing cache
                cache.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    public static setResource(resource: string): void {
        this.resource = resource;
    }
}