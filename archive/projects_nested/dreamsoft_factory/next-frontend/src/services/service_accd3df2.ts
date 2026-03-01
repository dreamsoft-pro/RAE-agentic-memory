import api from '@/lib/api';
import { Cache } from 'your-cache-library'; // Assuming you have a cache library or object defined somewhere

export default class FormatService {
    private cache: Cache; // Define cache as a property of the class

    constructor(cacheInstance: Cache) {
        this.cache = cacheInstance;
    }

    async getResource(resource: string, force?: boolean): Promise<any> {
        const cachedData = await this.cache.get(resource);

        if (cachedData && !force) {
            return cachedData;
        } else {
            try {
                const data = await api.get(`/api/${resource}`);
                await this.cache.put(resource, data);
                return data;
            } catch (error) {
                throw error; // Ensure the rejection is handled as a thrown error
            }
        }
    }

    async getCustomNames(): Promise<any> {
        const resource = 'ps_formats';
        try {
            const customNameData = await api.get(`/api/${resource}/customName?typeID=${this.typeID}`);
            return customNameData;
        } catch (error) {
            throw error; // Ensure the rejection is handled as a thrown error
        }
    }

    set typeID(id: number) {
        this._typeID = id;
    }

    get typeID(): number {
        return this._typeID;
    }

    private _typeID: number;

    constructor() {
        this.typeID = 0; // Set default value for typeID
    }
}