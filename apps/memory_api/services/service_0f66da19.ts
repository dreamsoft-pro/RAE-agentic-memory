import api from '@/lib/api';

export default class OngoingService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async getSettings(): Promise<any> {
        try {
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/productionSettings`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    async saveSettings(data: any): Promise<any> {
        try {
            const url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/productionSettings`;
            const response = await api.put(url, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}