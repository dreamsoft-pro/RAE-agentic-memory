import api from '@/lib/api';

class DeviceService {

    static async getDeviceSkills(resource: string, deviceID: string): Promise<any> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${[resource, deviceID, 'deviceSkills'].join('/')}`;
        
        try {
            const response = await api.get(url);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error: any) {
            throw error;
        }
    }

    static async same(deviceID: string): Promise<any> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${[this.resource, 'sameDevices', deviceID].join('/')}`;

        try {
            const response = await api.get(url);
            return response.data;
        } catch (error: any) {
            throw error;
        }
    }

    static setSame(deviceID: string, devices: any[]): Promise<void> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${[this.resource, deviceID].join('/')}`;

        return new Promise((resolve, reject) => {
            api.post(url, { devices })
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }

    private static resource: string = 'your-resource-string-here'; // Define your resource here

}

// Usage Example
export default DeviceService;