import api from '@/lib/api';

class DeviceService {

    private async addSpeed(deviceId: string, speedData: any): Promise<any> {
        try {
            const response = await api.post([resource, deviceId, 'deviceSpeeds'].join("/"), speedData);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    private async deleteSpeed(deviceId: string, speedId: string): Promise<void> {
        try {
            await api.delete([resource, deviceId, 'deviceSpeeds', speedId].join("/"));
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}

// Usage example
const deviceService = new DeviceService();

// Ensure resource is defined before using it
let resource: string;

if (!resource) {
    console.error('Resource must be defined');
    process.exit(1);
}

deviceService.addSpeed("some-device-id", { /* speed data */ })
    .then(data => console.log(data))
    .catch(error => console.error(error));

deviceService.deleteSpeed("some-device-id", "speed-id")
    .catch(error => console.error(error));