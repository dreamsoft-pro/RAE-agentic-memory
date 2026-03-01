import api from '@/lib/api';

class DeviceService {

    private resource: string = 'someResource'; // Define this as needed

    static async deleteDevicePrice(deviceID: number, priceID: number): Promise<any> {
        try {
            const response = await api.delete(`${this.resource}/${deviceID}/devicePrices/${priceID}`);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Response error');
            }
        } catch (error) {
            throw error;
        }
    }

    static async getSettings(deviceID: number): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/${deviceID}/deviceSettings`);
            return response.data;
        } catch (error) {
            throw new Error('Failed to fetch settings');
        }
    }
}

// Example usage in a Next.js page or component
export default function MyPage() {
    DeviceService.deleteDevicePrice(1, 2)
        .then(data => console.log('Deleted price data:', data))
        .catch(error => console.error('Error deleting price:', error));

    DeviceService.getSettings(3)
        .then(settings => console.log('Device settings:', settings))
        .catch(error => console.error('Failed to get settings:', error));
}