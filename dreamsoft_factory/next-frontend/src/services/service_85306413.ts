import api from '@/lib/api';

class DeviceService {
    private static async patchSameDevices(resource: string, deviceID: number, devices: any): Promise<any> {
        const url = `${process.env.API_URL}/${resource}/sameDevices/${deviceID}`;
        try {
            const response = await api.patch(url, { data: devices });
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Network error');
        }
    }

    private static async countOngoings(resource: string): Promise<number> {
        const url = `${process.env.API_URL}/${resource}/countOngoings?date=${new Date().getTime()}`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Network error');
        }
    }

    private static async countOngoingsPlanned(resource: string): Promise<number> {
        // Assuming 'countOngoingPlanned' function has a similar implementation pattern
        const url = `${process.env.API_URL}/${resource}/countOngoingPlanned?date=${new Date().getTime()}`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error('Network error');
        }
    }

    static async performPatch(resource: string, deviceID: number, devices: any): Promise<any> {
        return DeviceService.patchSameDevices(resource, deviceID, devices);
    }

    static async getOngoingCount(resource: string): Promise<number> {
        return DeviceService.countOngoings(resource);
    }

    static async getPlannedCount(resource: string): Promise<number> {
        return DeviceService.countOngoingsPlanned(resource);
    }
}

// Usage example:
// const ongoingCount = await DeviceService.getOngoingCount('yourResourceName');