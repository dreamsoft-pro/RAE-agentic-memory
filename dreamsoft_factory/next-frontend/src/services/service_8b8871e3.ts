import api from '@/lib/api';

class PromotionService {
    private resource: string = 'promotions'; // Assuming promotions as a placeholder for your actual resource

    public async update(data: any): Promise<any> {
        try {
            const response = await api.put(`${$config.API_URL}/${this.resource}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async remove(id: string): Promise<void> {
        try {
            const response = await api.delete(`${$config.API_URL}/${[this.resource, id].join("/")}`);
            if (!response.data.response) {
                console.log(response.data.message);
            }
        } catch (error) {
            throw error;
        }
    }
}

export default PromotionService;