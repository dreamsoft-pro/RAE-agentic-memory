import api from '@/lib/api';

class DeviceService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async deleteDevice(deviceID: string, id: string): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${this.resource}/${deviceID}/deviceServices/${id}`;
            const response = await api.delete(url);
            return response.data.response ? response.data : Promise.reject(response.data);
        } catch (error) {
            throw error;
        }
    }

    public async getWorkUnits(): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${this.resource}/getWorkUnits`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default DeviceService;