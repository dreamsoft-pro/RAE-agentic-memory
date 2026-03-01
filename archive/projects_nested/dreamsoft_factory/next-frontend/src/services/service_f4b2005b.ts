import api from "@/lib/api";
import { Cache } from "@/utils/cache"; // Assuming there's a cache utility in place

class PromotionService {
    private resource: string;
    private url: string;
    private cache: Cache;

    constructor(resource: string, cache: Cache) {
        this.resource = resource;
        this.url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`;
        this.cache = cache;
    }

    async fetchCollection(force?: boolean): Promise<any> {
        let cachedData = force ? undefined : this.cache.get('collection');

        if (cachedData && !force) {
            return cachedData;
        } else {
            try {
                const response = await api.get(this.url);
                const data = response.data;

                this.cache.put('collection', data);
                // Simulating $rootScope.$emit with a custom event emitter or context updating mechanism
                // For simplicity, let's just log the event here.
                console.log(`Emitting promotions.getAll with data: ${JSON.stringify(data)}`);

                return data;
            } catch (error) {
                throw new Error(JSON.stringify(error));
            }
        }
    }

    async getAll(): Promise<any> {
        try {
            const response = await api.get(this.url);
            const data = response.data;

            // Simulating $rootScope.$emit with a custom event emitter or context updating mechanism
            console.log(`Emitting promotions.getAll with data: ${JSON.stringify(data)}`);

            return data;
        } catch (error) {
            throw new Error(JSON.stringify(error));
        }
    }
}

export default PromotionService;