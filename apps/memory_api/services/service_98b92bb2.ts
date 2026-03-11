import api from '@/lib/api';
import { CacheService } from '@/services/cache'; // Assuming you have a cache service defined somewhere

class TypeService {

    static async forView(groupUrl: string, force: boolean = false): Promise<any> {
        if (CacheService.get(`collection${groupUrl}`) && !force) {
            return CacheService.get(`collection${groupUrl}`);
        }

        try {
            const response = await api.get(`/ps_groups/${groupUrl}/ps_types/forView`);
            const data = response.data;
            CacheService.put(`collection${groupUrl}`, data);
            return data;
        } catch (error) {
            throw error;
        }
    }

    static async getOneForView(groupUrl: string, typeUrl?: string): Promise<any> {
        if (typeof groupUrl === 'undefined') {
            groupUrl = '';
        }

        try {
            const response = await api.get(`/ps_groups/${groupUrl}/ps_types/${typeUrl || ''}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}