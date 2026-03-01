import api from "@/lib/api";
import { Cache } from "@/utils/cache"; // Assuming a cache utility exists

class LangSettingsService {
    private static async getAll(cache: Cache, resource: string, force = false): Promise<any> {
        if (cache.get('collection') && !force) {
            const data = cache.get('collection');
            this.getAllDef.resolve(data);
            return data;
        } else {
            try {
                const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}/${resource}`);
                cache.put('collection', response.data);
                this.getAllDef.resolve(response.data);
                return response.data;
            } catch (error) {
                this.getAllDef.reject(error);
                throw error; // Rethrow to handle the rejection
            }
        }

        return this.getAllDef.promise;
    }

    private static getAllDef = Promise.defer(); // Assuming a deferred promise setup somewhere in your class

    public static async create(lang: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}/resource`, lang); // Adjust the resource as needed
            return response.data;
        } catch (error) {
            throw error; // Rethrow to handle the rejection
        }
    }

    // Other methods...
}

// Usage example:
(async () => {
    const cache = new Cache(); // Initialize your cache here
    try {
        const data = await LangSettingsService.getAll(cache, 'resource');
        console.log(data);
    } catch (error) {
        console.error(error);
    }
})();