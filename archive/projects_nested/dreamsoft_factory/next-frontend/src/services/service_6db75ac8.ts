import api from '@/lib/api';
import { CacheService } from '@/services/CacheService'; // Assuming cache service is defined elsewhere

class PsConfigAttribute {
    static async edit(item: any): Promise<any> {
        try {
            const response = await api.put(`/resources/${resource}`, item);
            if (response.data.response) {
                CacheService.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }

    static async remove(item: any): Promise<any> {
        try {
            const response = await api.delete(`/resources/${resource}/${item.ID}`);
            if (response.data.response) {
                CacheService.remove('collection');
                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error) {
            throw error;
        }
    }
}

// Ensure the 'resource' variable is defined before using it in PsConfigAttribute methods.
const resource = 'your-resource-name'; // Define this or pass as a parameter