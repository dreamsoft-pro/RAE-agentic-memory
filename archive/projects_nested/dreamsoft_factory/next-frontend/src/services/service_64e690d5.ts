import api from '@/lib/api';
import { Cache } from 'tiny-invariant'; // Assuming you will manage caching in a similar way, replace with actual cache module if different

export default class PsTypeService {
    private cache: Map<string, any>;

    constructor() {
        this.cache = new Map();
    }

    async getAll(groupID: string | number, force: boolean): Promise<any[]> {
        const key = `collection${groupID}`;

        if (!force && this.cache.has(key)) {
            return this.cache.get(key);
        } else {
            try {
                const data = await api.get(`/ps_groups/${groupID}/ps_types`);
                const plainData = data.data.map(item => item); // Assuming .plain() behavior
                this.cache.set(key, plainData);
                return plainData;
            } catch (error) {
                throw error;
            }
        }
    }
}