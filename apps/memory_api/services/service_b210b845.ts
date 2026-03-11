import api from "@/lib/api";

class DeviceService {
    static async sortResources(resource: string, sort: any): Promise<any> {
        const url = `${process.env.API_URL}/${[resource, 'sort'].join('/')}`;
        try {
            const response = await api.patch(url, sort);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    static async getSpeeds(deviceID: string): Promise<any> {
        const url = `${process.env.API_URL}/${[resource, deviceID, 'deviceSpeeds'].join('/')}`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    // Ensure 'resource' is defined before use
    private static resource: string | null = null;

    static setResource(value: string): void {
        this.resource = value;
    }
}

// Usage example:
DeviceService.setResource('example-resource');
DeviceService.sortResources('example-resource', { sortKey: 'value' })
    .then(data => console.log(data))
    .catch(error => console.error(error));

DeviceService.getSpeeds('123')
    .then(data => console.log(data))
    .catch(error => console.error(error));