import api from '@/lib/api';

class PsConfigOption {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async getPrices(optID: string, controllerID: string): Promise<any[]> {
        const url = `${this.getResource()}/${optID}/priceControllers/${controllerID}/ps_prices`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error(error.message);
        }
    }

    async getDiscountPrices(optID: string, controllerID: string, discountGroupID: string): Promise<any[]> {
        const url = `${this.getResource()}/${optID}/priceControllers/${controllerID}/ps_prices/discountPrices/${discountGroupID}`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : new Error(error.message);
        }
    }

    private getResource(): string {
        // Implement this method as per your application logic
        return this.resource; // This is just a placeholder
    }
}