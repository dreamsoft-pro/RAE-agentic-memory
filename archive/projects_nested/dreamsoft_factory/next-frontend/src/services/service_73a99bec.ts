import api from "@/lib/api";

class DeviceService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async saveSettings(deviceID: string, data: any): Promise<any> {
        try {
            const response = await api.put(`${this.resource}/${deviceID}/deviceSettings`, data);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error;
        }
    }

    async getServices(deviceID: string): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/${deviceID}/deviceServices`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default DeviceService;