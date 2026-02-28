import api from '@/lib/api';

class ShiftService {
    static async getAllFromDevice(deviceID: string): Promise<any> {
        const url = `${process.env.API_URL}/${deviceResource}/${deviceID}`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    static async createForDevice(data: any): Promise<any> {
        const url = `${process.env.API_URL}/${deviceResource}`;
        try {
            const response = await api.post(url, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    static async updateOnDevice(module: any): Promise<any> {
        var def = new Promise((resolve, reject) => {
            try {
                const url = `${process.env.API_URL}/${deviceResource}`;
                api.put(url, module).then(response => resolve(response.data))
                    .catch(error => reject(error.response ? error.response : error));
            } catch (error) {
                reject(error);
            }
        });
        return def;
    }

    // Ensure deviceResource is defined before use
    static get deviceResource(): string | undefined {
        if (!deviceResource) { throw new Error('Device resource must be set'); }
        return deviceResource; // This should be properly initialized elsewhere in your application
    }
}

// Initialization of necessary variables would happen outside this class definition or within a constructor.