import api from '@/lib/api';

class DeviceService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async countOngoingsPlanned(): Promise<number> {
        try {
            const response = await api.get(`${this.resource}/countOngoingsPlanned`);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data || 'An error occurred');
        }
    }

    async countFilteredOngoings(deviceID: string, finished: boolean): Promise<number> {
        try {
            const urlParam = `?deviceID=${deviceID}&finished=${finished}`;
            const response = await api.get(`${this.resource}/countFilteredOngoings${urlParam}`);
            return response.data;
        } catch (error) {
            throw new Error(error.response?.data || 'An error occurred');
        }
    }

    // The sort function is incomplete in the provided code, so I'm leaving it with a placeholder.
    async sort(sort: string): Promise<void> {
        try {
            const response = await api.get(`${this.resource}/sort`);
            // Handle sorting logic based on response
        } catch (error) {
            throw new Error(error.response?.data || 'An error occurred');
        }
    }
}

export default DeviceService;