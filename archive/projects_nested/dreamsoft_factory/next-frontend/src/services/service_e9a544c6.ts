import api from '@/lib/api';

export default class OngoingService {

    static async patchLogs(isAdditional: boolean, resource: string, ongoingID: string): Promise<any> {
        const path = isAdditional ? 'logsAdditional' : 'logs';
        
        try {
            const response = await api.get(`${resource}/${path}/${ongoingID}`);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    static async patchWorkplace(workplace: any): Promise<any> {
        try {
            const response = await api.patch('workplaces', workplace);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }
}