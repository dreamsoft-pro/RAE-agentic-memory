import api from "@/lib/api";

class IncreaseService {
    private resource: string;
    private url: string;

    constructor(resource: string, url: string) {
        this.resource = resource;
        this.url = url;
    }

    async remove(item: { ID: number }) {
        try {
            const response = await api.patch(`${this.url}/${item.ID}`, { remove: item.ID });
            if (response.data.response) {
                // Assuming cache.remove is a function that removes an entry from the cache
                this.cacheRemove(this.resource);
                return response.data;
            } else {
                throw new Error('Response was not as expected');
            }
        } catch (error) {
            throw error;
        }
    }

    private cacheRemove(resource: string): void {
        // Implement your caching logic here
        console.log(`Cache entry for ${resource} removed`);
    }
}

export default IncreaseService;