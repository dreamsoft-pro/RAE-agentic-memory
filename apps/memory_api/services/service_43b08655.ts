import api from '@/lib/api';
import { Cache } from 'next/cache'; // Assuming some kind of caching mechanism

class RealizationTimeService {
    private cache: Record<string, any> = {};

    public async getAll(force?: boolean): Promise<any[]> {
        if (this.cache['collection'] && !force) {
            return this.cache['collection'];
        }

        try {
            const response = await api.get('/ps_realizationTimes');
            if (response.data) {
                this.cache['collection'] = response.data.plain();
                return this.cache['collection'];
            } else {
                throw new Error('No data returned from API');
            }
        } catch (error: any) {
            console.error('Error fetching realization times:', error);
            throw error;
        }
    }
}

export default RealizationTimeService;

// Example usage
const service = new RealizationTimeService();
service.getAll().then(data => console.log('Realization Times:', data)).catch(error => console.error('Failed to fetch data:', error));