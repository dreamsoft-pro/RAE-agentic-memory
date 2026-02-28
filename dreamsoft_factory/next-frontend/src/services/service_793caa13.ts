import api from '@/lib/api';

class OngoingService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource; // Ensure 'resource' is defined before usage.
    }

    public async getAllOperatorLogs(dates: any): Promise<any> {
        try {
            const response = await api.post(`${this.resource}/getAllOperatorLogs`, dates);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async getDeviceLogs(deviceID: string, dates: any): Promise<any> {
        try {
            const response = await api.post(`${this.resource}/getDeviceLogs/${deviceID}`, dates);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}