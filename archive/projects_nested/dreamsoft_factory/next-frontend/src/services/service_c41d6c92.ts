import api from '@/lib/api';

export default class RealizationTimeService {
    private static async sort(sort: any): Promise<any> {
        try {
            const response = await api.patch(`/ps_realizationTimes/sort`, sort);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Sorting failed');
            }
        } catch (error) {
            throw error;
        }
    }

    private static async remove(item: any): Promise<any> {
        try {
            const response = await api.delete(`/ps_realizationTimes/${item.id}`);
            if (response.data.response) {
                return response.data;
            } else {
                throw new Error('Removal failed');
            }
        } catch (error) {
            throw error;
        }
    }

    // Add any other methods here
}