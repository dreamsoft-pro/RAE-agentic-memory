import api from '@/lib/api';

class TaxService {
    private cache: Map<string, any> = new Map();
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async getAll(force?: boolean): Promise<any[]> {
        if (this.cache.get('collection') && !force) {
            return this.cache.get('collection');
        } else {
            try {
                const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}${this.resource}`);
                this.cache.set('collection', response.data);
                // Emulating the original event emitting logic (not directly supported in Next.js/React, but you could use other state management solutions)
                console.log('Tax.getAll:', response.data); 
                return response.data;
            } catch (error) {
                throw error;  // or handle error as needed
            }
        }
    }

    public create(lang: string): Promise<void> {
        const def = Promise.resolve();  // Example placeholder, you might want to define actual logic here.
        
        // Since this is an example and the original code didn't specify what `create` method does,
        // I've used a simple resolved promise as an example. You should implement your specific logic here.

        return def;
    }
}

export default TaxService;

// Example usage:
const taxService = new TaxService('yourResource');
taxService.getAll().then(data => console.log(data));