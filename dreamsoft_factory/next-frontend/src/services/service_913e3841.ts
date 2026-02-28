import api from '@/lib/api';
import { Cache } from 'your-cache-library'; // Replace with actual cache library import

class VolumeService {
    private resource: string;
    private cache: Cache;

    constructor(resource: string, cache: Cache) {
        this.resource = resource;
        this.cache = cache;
    }

    public async getCustom(force?: boolean): Promise<any> {
        const resource = `${this.resource}/customVolume`;

        if (force || !this.cache.has(resource)) {
            try {
                const data = await api.get(resource);
                this.cache.put(resource, data.plain());
                return data.plain();
            } catch (error) {
                throw error;
            }
        }

        return this.cache.get(resource);
    }

    public async setCustom(value: any): Promise<any> {
        try {
            const data = await api.patch(this.resource, { action: 'setCustomVolume', custom: value });
            if (!data.response) {
                throw new Error('Data response not valid');
            }
            this.cache.remove(this.resource);
            return data;
        } catch (error) {
            throw error;
        }
    }
}