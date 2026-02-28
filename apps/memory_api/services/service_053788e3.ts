import api from '@/lib/api';

class ShiftService {
    static async sort(sort: any): Promise<any> {
        const resource = 'your-device-resource'; // Replace 'your-device-resource' with your actual deviceResource variable.
        try {
            const response = await api.patch(`${process.env.API_URL}/${[resource, 'sort'].join('/')}`, sort);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    static async copyFrom(data: any): Promise<any> {
        const resource = 'your-device-resource'; // Replace 'your-device-resource' with your actual deviceResource variable.
        try {
            const response = await api.post(`${process.env.API_URL}/${[resource, 'copyFrom'].join('/')}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }
}

export default ShiftService;