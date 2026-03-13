import api from '@/lib/api';
import { CacheService } from '@/services/cache'; // Assuming this is a cache service you have

class TypeService {
    static async remove(groupID: number, item: { ID: string | number }) {
        const resource = `ps_groups/${groupID}/ps_types`;
        try {
            await api.delete(`${resource}/${item.ID}`);
            CacheService.remove(`collection${groupID}`); // Remove cache
            return Promise.resolve({ data }); // Assuming 'data' is what you want to resolve
        } catch (error) {
            return Promise.reject(error);
        }
    }

    static async sort(groupID: number, sort: any) { // Replace 'any' with the actual type of sort object
        const resource = `ps_groups/${groupID}/ps_types`;
        try {
            await api.patch(`${resource}/sort`, sort);
            CacheService.remove(`collection${groupID}`); // Remove cache
            return Promise.resolve({ data }); // Assuming 'data' is what you want to resolve
        } catch (error) {
            return Promise.reject(error);
        }
    }
}

export default TypeService;