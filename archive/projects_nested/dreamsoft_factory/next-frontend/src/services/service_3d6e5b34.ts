import api from '@/lib/api';

class CurrencyService {
    private cache: Map<string, any>;
    private resource: string;
    private url: string;

    constructor(cache: Map<string, any>, resource: string) {
        this.cache = cache;
        this.resource = resource;
        this.url = `${process.env.API_URL}/${this.resource}`;
    }

    async getAll(force?: boolean): Promise<any> {
        const cachedData = force ? undefined : this.cache.get('collection');
        if (cachedData !== undefined && !force) {
            return cachedData;
        } else {
            try {
                const response = await api.get(this.url);
                this.cache.set('collection', response.data);
                // Assuming $rootScope.$emit is a custom function for event emission
                this.emitEvent('Currency.getAll', response.data);
                return response.data;
            } catch (error) {
                throw error;
            }
        }
    }

    private emitEvent(eventName: string, eventData: any): void {
        // Custom logic to emit an event
        console.log(`Emitting event ${eventName} with data`, eventData);
    }

    create(lang: string): Promise<any> {
        return new Promise((resolve, reject) => {
            this.getAll().then(data => {
                resolve(data);
            }).catch(error => {
                reject(error);
            });
        });
    }
}

export default CurrencyService;