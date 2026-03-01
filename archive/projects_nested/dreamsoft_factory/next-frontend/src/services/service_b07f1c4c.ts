import api from '@/lib/api';

class OngoingService {
    static async patchOperator(operator: any): Promise<any> {
        const resource = 'your-resource-name'; // Define your resource here
        try {
            const response = await api.patch(`${resource}/operator`, operator);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error;
        }
    }
}