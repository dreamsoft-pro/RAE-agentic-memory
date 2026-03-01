import api from "@/lib/api";

class DeviceService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async deleteDeviceSideRelation(deviceID: number, id: number): Promise<any> {
        try {
            const response = await api.delete(`${this.resource}/${deviceID}/deviceSideRelations/${id}`);
            return response.data.response ? response.data : Promise.reject(response.data);
        } catch (error) {
            return Promise.reject(error);
        }
    }

    async getPrices(deviceID: number): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/${deviceID}/devicePrices`);
            return response.data;
        } catch (error) {
            return Promise.reject(error);
        }
    }
}

// Usage example:
const deviceService = new DeviceService('yourResource');
deviceService.deleteDeviceSideRelation(1, 2).then(data => console.log(data)).catch(err => console.error(err));
deviceService.getPrices(3).then(prices => console.log(prices)).catch(err => console.error(err));