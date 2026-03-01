javascript
import { BackendApi } from '@/lib/api';
import { CacheService } from './cache.service';

const cacheKey = 'ps_priceLists';

class PsPricelistService {
    constructor(private backend: BackendApi, private cacheService: CacheService) {}

    getUploadUrl(priceListID: string): string {
        return `${this.backend.getBaseUrl()}ps_priceLists/uploadIcon/${priceListID}`;
    }

    getAll(force?: boolean): Promise<any> {
        if (!force && this.cacheService.exists(cacheKey)) {
            return Promise.resolve(this.cacheService.get(cacheKey));
        }
        
        return this.backend.getAll('ps_priceLists').then((response: any) => {
            this.cacheService.set(cacheKey, response);
            return response;
        });
    }
}

// [BACKEND_ADVICE] Heavy logic should be offloaded to the backend service for better separation of concerns.

export { PsPricelistService };
