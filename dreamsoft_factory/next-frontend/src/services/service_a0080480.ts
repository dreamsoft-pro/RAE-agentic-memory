import api from '@/lib/api';

class DeviceService {
    private apiUrl: string;

    constructor(config: { API_URL: string }) {
        this.apiUrl = config.API_URL;
    }

    async saveSpeedChange(deviceID: number, data: any): Promise<any> {
        try {
            const response = await api.post(
                `${this.apiUrl}/${resource}/${deviceID}/deviceSpeedChanges`,
                data
            );
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error: any) {
            console.error(error);
            throw error;
        }
    }

    async deleteSpeedChange(deviceID: number, id: number): Promise<any> {
        try {
            const response = await api.delete(
                `${this.apiUrl}/${resource}/${deviceID}/deviceSpeedChanges/${id}`
            );
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error: any) {
            console.error(error);
            throw error;
        }
    }
}

// Example usage:
const config = { API_URL: 'http://example.com/api' };
const deviceService = new DeviceService(config);

deviceService.saveSpeedChange(1, { speed: 50 }).then((data) => {
    // Handle success
}).catch((error) => {
    // Handle error
});

deviceService.deleteSpeedChange(1, 2).then((data) => {
    // Handle success
}).catch((error) => {
    // Handle error
});