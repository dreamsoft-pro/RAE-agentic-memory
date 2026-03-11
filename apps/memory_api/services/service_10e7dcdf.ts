import api from '@/lib/api';
import { CacheService } from '@/services/cache'; // Assuming a CacheService exists

class RealizationTimeService {
    private cache: any; // Assuming CacheService has remove method

    constructor() {
        this.cache = new CacheService(); // Initialize the CacheService
    }

    async edit(item: any): Promise<any> {
        try {
            const response = await api.put('ps_realizationTimes', item);
            if (response.data.response) { // Adjust based on actual API response structure
                this.cache.remove('collection');
                return response.data;
            } else {
                throw new Error(response.data); // Handle error appropriately in calling code
            }
        } catch (error) {
            throw error; // Re-throw or handle errors as needed
        }
    }

    async add(item: any): Promise<any> {
        try {
            const response = await api.post('ps_realizationTimes', item);
            if (response.data.ID) { // Adjust based on actual API response structure
                this.cache.remove('collection');
                return response.data;
            } else {
                throw new Error(response.data); // Handle error appropriately in calling code
            }
        } catch (error) {
            throw error; // Re-throw or handle errors as needed
        }
    }
}

export default RealizationTimeService;

// Usage Example:
const realizationTimeService = new RealizationTimeService();
realizationTimeService.edit({ /* item data */ }).then(data => console.log('Edited: ', data))
.catch(error => console.error('Error:', error));

realizationTimeService.add({ /* item data */ }).then(data => console.log('Added: ', data))
.catch(error => console.error('Error:', error));