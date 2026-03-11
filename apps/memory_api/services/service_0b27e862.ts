import api from '@/lib/api';
import { AxiosResponse } from 'axios';

class DeviceService {
    private static async ongoingSort(deviceID: string, sort: any): Promise<AxiosResponse> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/${deviceID}/deviceOngoings/sort`;

        try {
            const response = await api.patch(url, sort);
            if (response.data.response) {
                return response;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error;
        }
    }

    private static async ongoingMove(deviceID: string, ongoingID: string, newDeviceID: string): Promise<AxiosResponse> {
        const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/${deviceID}/ongoing/${ongoingID}/moveTo/${newDeviceID}`;

        try {
            const response = await api.patch(url);
            if (response.data.response) {
                return response;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error;
        }
    }

    // Add getters or methods to call these static functions as needed.
}

// Example usage:
// DeviceService.ongoingSort(deviceID, sortData).then(response => console.log(response)).catch(error => console.error(error));