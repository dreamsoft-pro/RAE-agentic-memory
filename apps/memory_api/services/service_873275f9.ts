import api from '@/lib/api';

class DeviceService {
    static async addPrice(deviceID: string, priceData: any): Promise<any> {
        const resource = 'devices'; // Ensure the variable is defined before use
        try {
            const url = `${process.env.API_URL}/${[resource, deviceID, 'devicePrices'].join('/')}`;
            const response = await api.post(url, priceData);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error; // Rethrow the error to maintain promise rejection
        }
    }

    static async deletePrice(deviceID: string, priceID: string): Promise<void> {
        const resource = 'devices'; // Ensure the variable is defined before use
        try {
            const url = `${process.env.API_URL}/${[resource, deviceID, 'devicePrices', priceID].join('/')}`;
            await api.delete(url);
        } catch (error) {
            throw error; // Rethrow the error to maintain promise rejection
        }
    }
}