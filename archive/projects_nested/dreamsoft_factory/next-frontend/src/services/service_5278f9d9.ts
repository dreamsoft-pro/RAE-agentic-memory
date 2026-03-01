import api from '@/lib/api';
import { Cache } from 'next/cache';

const cacheKey = 'ps_increase_types_collection';

class PsIncreaseTypeService {
    private static instance: PsIncreaseTypeService;
    
    private constructor() {}

    public static getInstance(): PsIncreaseTypeService {
        if (!PsIncreaseTypeService.instance) {
            PsIncreaseTypeService.instance = new PsIncreaseTypeService();
        }
        return PsIncreaseTypeService.instance;
    }

    public async getAll(force?: boolean): Promise<any[]> {
        let collection: any[];

        // Check cache and use it if available
        if (force === false && cacheKey in Cache) {
            collection = Cache.get(cacheKey);
        } else {
            try {
                const response = await api.get('ps_increase_types');
                collection = response.data;
                Cache.set(cacheKey, collection);

                if (force === true) {
                    // Emit event or perform equivalent action
                }
            } catch (error) {
                throw error; // Handle error as needed
            }
        }

        return collection;
    }
}

export default PsIncreaseTypeService.getInstance();