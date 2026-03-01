import api from '@/lib/api';

export class OngoingService {
    private resource: string = 'your-resource-name'; // Define this property as per your requirement

    public async patchTaskWorkplaces(workplace: any): Promise<any> {
        try {
            const response = await api.patch(`${this.resource}/taskWorkplaces`, workplace);
            return response.data.response ? response.data : Promise.reject(response.data);
        } catch (error) {
            throw error;
        }
    }

    public async getTaskWorkplaces(itemID: string): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/taskWorkplaces/${itemID}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}