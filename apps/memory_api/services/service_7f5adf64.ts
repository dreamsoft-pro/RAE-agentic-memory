import api from '@/lib/api';

class AuctionService {

    private static async update(offer: any): Promise<any> {
        try {
            const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${offer.resource}`, offer.data);
            
            if (response.data.response) {
                // Assuming cache is a module or service that can be imported
                import('@/cache').then(cacheModule => {
                    cacheModule.cache.remove('collection');
                });

                return response.data;
            } else {
                throw new Error(JSON.stringify(response.data));
            }
        } catch (error: any) {
            throw error;
        }
    }

    // Assuming you want to expose this method publicly
    public static async fetchUpdatedOffer(offer: any): Promise<any> {
        try {
            const result = await AuctionService.update(offer);
            return result;
        } catch (error) {
            console.error('Failed to update offer:', error.message);
            throw error;  // Optionally re-throw if you need the caller to handle this
        }
    }

}

export default AuctionService;

// Usage Example:
// import AuctionService from './path-to-auction-service';
// const updatedOffer = await AuctionService.fetchUpdatedOffer({ resource: 'someResource', data: {} });