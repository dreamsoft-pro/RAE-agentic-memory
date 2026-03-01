import { RestService } from '@/lib/api'; // Assuming 'api' module exports this service

export default class PsPricelistService {
    private cache: any; // Replace `any` with proper type if known
    private restService: RestService;

    constructor(cache: any, restService: RestService) {
        this.cache = cache;
        this.restService = restService;
    }

    async fetchCollection(force?: boolean): Promise<any[]> {
        let collection: any[] | undefined = force ? undefined : this.cache.get('collection');
        
        if (typeof collection !== 'undefined') return collection;

        try {
            const data = await this.restService.all('ps_priceLists').getList();
            const collection = data.plain();

            this.cache.put('collection', collection);

            if (force) {
                // Assuming there's a way to emit events in Next.js context
                // If not, you may need to adjust or remove this line.
                window.dispatchEvent(new CustomEvent('ps_priceLists', { detail: collection }));
            }

            return collection;
        } catch (error) {
            throw error; // Consider adding more specific handling if needed
        }
    }

    async addItem(item: any): Promise<any[]> {
        try {
            const data = await this.restService.all('ps_priceLists').doPOST(item);
            const collection = data.plain();
            
            return collection;
        } catch (error) {
            throw error; // Consider adding more specific handling if needed
        }
    }
}