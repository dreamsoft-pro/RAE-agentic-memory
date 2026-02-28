import api from '@/lib/api';
import { Cache } from 'next/cache';

export default class PsConfigOptionService {
    private cache: Cache;

    constructor() {
        this.cache = new Map<string, any>();
    }

    public async getAll(attrID: string | number, force?: boolean): Promise<any> {
        const resource = `ps_attributes/${attrID}/ps_options`;
        if (!force && this.cache.has(resource)) {
            return this.cache.get(resource);
        }
        
        try {
            const response = await api.get(resource);
            this.cache.set(resource, response.data); // Assuming we store the fetched data in cache
            return response.data;
        } catch (error) {
            throw new Error(`Failed to fetch options for attribute ${attrID}: ${error.message}`);
        }
    }

    public async getUploadUrl(attrID: string | number): Promise<string> {
        const resource = `ps_attributes/${attrID}/ps_options/uploadIcon`;
        return `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
    }

    public createPsConfigOption(attrID: string | number) {
        return new PsConfigOption(attrID);
    }
}

class PsConfigOption {
    private attrID: string | number;

    constructor(attrID: string | number) {
        this.attrID = attrID;
    }

    public getResource(): string {
        return `ps_attributes/${this.attrID}/ps_options`;
    }
}