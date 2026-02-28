import api from '@/lib/api';

class CurrencyRootService {
    private cache: { [key: string]: any };
    private resource: string;
    
    constructor(cache: { [key: string]: any }, resource: string) {
        this.cache = cache;
        this.resource = resource;
    }

    async getAll(force?: boolean): Promise<any> {
        const cachedData = force ? null : this.cache.get('collection');
        
        if (cachedData !== undefined && !force) {
            return cachedData;
        } else {
            try {
                const url = `${process.env.API_URL}/${this.resource}`;
                const response = await api.get(url);
                this.cache.put('collection', response.data);

                // Assuming $rootScope.$emit is a custom event emitter function
                // Replace with actual event emitting logic in Next.js environment.
                emitCurrencyEvent(response.data); 

                return response.data;
            } catch (error) {
                throw error.response ? error.response : error;
            }
        }
    }

    create(lang: string): Promise<any> {
        const def = Promise.resolve();
        
        // Assuming this is where you would handle the creation logic,
        // but since it's incomplete, we're just returning a resolved promise.
        return def;
    }
}

// Helper function to emit an event similar to $rootScope.$emit in Next.js context
function emitCurrencyEvent(data: any) {
    console.log('Emitting CurrencyRoot.getAll with data:', data);
}

export default CurrencyRootService;