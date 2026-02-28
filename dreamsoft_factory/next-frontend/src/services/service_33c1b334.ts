import api from '@/lib/api';

class PsConfigOption {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async fetchList(): Promise<void> {
        try {
            const data = await api.get(this.getResource());
            // Assuming cache is defined elsewhere in the class
            this.cache.remove(this.resource);
        } catch (error) {
            throw error;
        }
    }

    private getResource(): string {
        return this.resource;
    }

    async savePrices(optID: string, controllerID: string, item: any): Promise<void> {
        const resource = `${this.getResource()}/${optID}/priceControllers/${controllerID}/ps_prices`;
        
        try {
            await api.patch(resource, item);
        } catch (error) {
            throw error;
        }
    }

    async removePrice(optID: string, controllerID: string): Promise<void> {
        const resource = `${this.getResource()}/${optID}/priceControllers/${controllerID}/ps_prices`;
        
        try {
            await api.delete(resource);
        } catch (error) {
            throw error;
        }
    }
}