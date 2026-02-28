import api from '@/lib/api';
import { cache } from 'your-cache-module'; // Replace with actual import if needed

class RealizationTimeService {
    async removeRealizationTime(item: { ID: number }): Promise<any> {
        const resource = 'ps_realizationTimes';

        try {
            const response = await api.delete(`${resource}/${item.ID}`);
            if (response.data.response) {
                cache.remove('collection');
                return response.data.plain();
            } else {
                throw new Error('Failed to remove realization time.');
            }
        } catch (error) {
            throw error;
        }
    }

    // Assuming you have a function that returns an instance of RealizationTimeService
}

export default new RealizationTimeService();