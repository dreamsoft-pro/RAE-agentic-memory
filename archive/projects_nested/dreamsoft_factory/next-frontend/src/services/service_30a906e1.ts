import api from "@/lib/api";

class AuctionService {
    private cache: Map<string, any>;
    
    constructor(cache: Map<string, any>) {
        this.cache = cache;
    }

    async getAll(force?: boolean): Promise<any> {
        const resource = 'someResource'; // Define your resource here

        if (this.cache.has('collection') && !force) {
            return this.cache.get('collection');
        } else {
            try {
                const data = await api.get(this.resourceUrl(resource));
                this.cache.set('collection', data);
                return data;
            } catch (error) {
                throw error;
            }
        }
    }

    getAuctions(filters: any): Promise<any> {
        return new Promise((resolve, reject) => {
            const resource = 'auctions'; // Define your resource here
            const url = this.resourceUrl(resource);
            
            if (filters) {
                const qs = new URLSearchParams(filters).toString();
                if (qs) {
                    url += '?' + qs;
                }
            }

            api.get(url)
                .then(response => resolve(response.data))
                .catch(error => reject(error));
        });
    }

    private resourceUrl(resource: string): string {
        return `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
    }
}

export default AuctionService;

// Usage Example:
const cache = new Map<string, any>();
const auctionService = new AuctionService(cache);

auctionService.getAll(false).then(data => console.log(data)).catch(error => console.error(error));
auctionService.getAuctions({ filter: 'value' }).then(data => console.log(data)).catch(error => console.error(error));