import api from '@/lib/api';
import { Cache } from '@/path/to/cache'; // Adjust import path according to your project structure

class PsConfigOption {
    private cache: Cache; // Assuming Cache is defined somewhere and used for caching purposes

    getResource(): string {
        // This method should return the resource string, replace with actual implementation
        throw new Error("Method not implemented");
    }

    async remove(item: { ID: number }): Promise<void> {
        const resource = this.getResource();

        try {
            const response = await api.delete(`${resource}/${item.ID}`);
            if (response.data) {
                this.cache.remove(resource);
            } else {
                throw new Error('Response data is not valid');
            }
        } catch (error) {
            throw error;
        }
    }

    async sort(sortList: any[]): Promise<void> {
        const resource = this.getResource();

        try {
            // Assuming there's an endpoint or method to handle sorting
            await api.post(`${resource}/sort`, { sortList });
            this.cache.remove(resource);
        } catch (error) {
            throw error;
        }
    }

    // Add other methods here as needed
}

export default PsConfigOption;