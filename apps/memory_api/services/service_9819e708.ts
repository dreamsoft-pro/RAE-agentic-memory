import api from '@/lib/api';
import { AxiosResponse } from 'axios';

class OngoingService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async saveProgress(data: any): Promise<AxiosResponse> {
        try {
            const response = await api.patch(`${this.resource}/progress`, data);
            return response;
        } catch (error) {
            throw error.response || error;
        }
    }

    public async sort(sort: any): Promise<AxiosResponse> {
        try {
            const response = await api.patch(`${this.resource}/sortProd`, sort);
            return response;
        } catch (error) {
            throw error.response || error;
        }
    }
}

export default OngoingService;