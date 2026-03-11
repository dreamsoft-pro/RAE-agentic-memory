import api from "@/lib/api";

class DiscountService {
    private cache: Map<string, any> = new Map();
    
    // Assuming force is passed as an argument and resource is available in context or constructor.
    public async getAll(force?: boolean): Promise<any[]> {
        if (!force && this.cache.has('collection')) {
            return this.cache.get('collection');
        }

        try {
            const response = await api.get(`${$config.API_URL}/${resource}`);
            const data = response.data;
            
            this.cache.set('collection', data);
            // Assuming $rootScope.$emit is a custom event emitter in your context.
            emitDiscountEvent(data); 
            return data;
        } catch (error) {
            throw error;  // You can also handle specific error cases here if needed
        }
    }

    public async getAllPromise(force?: boolean): Promise<any[]> {
        try {
            const response = await api.get(`${$config.API_URL}/${resource}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

// Example usage of event emitter function.
function emitDiscountEvent(data: any[]): void {
    // Implementation for emitting an event
}