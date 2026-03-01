import api from '@/lib/api';

class CurrencyService {
    private resource = '/currencies'; // Define the API resource

    async fetchCurrencies(): Promise<any[]> {
        try {
            const response = await api.get(this.resource);
            return response.data;
        } catch (error) {
            console.error('Failed to fetch currencies:', error);
            throw new Error('Unable to retrieve currency data.');
        }
    }

    private async getCurrencyById(id: string): Promise<any> {
        try {
            const url = `${this.resource}/${id}`; // Define the URL for a specific resource
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            console.error(`Failed to fetch currency with ID ${id}:`, error);
            throw new Error('Unable to retrieve currency data.');
        }
    }

    async getCurrencies(): Promise<any[]> {
        return this.fetchCurrencies();
    }

    async getCurrency(id: string): Promise<any> {
        return this.getCurrencyById(id);
    }
}

export default CurrencyService;