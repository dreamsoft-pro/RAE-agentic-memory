import api from '@/lib/api';

class AuctionService {
    private static async fetchIsAuctionUser(resource: string): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${resource}/isAuctionUser`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    public static async export(params: any): Promise<void | any> {
        try {
            const result = await AuctionService.fetchIsAuctionUser(params.resource);
            if (result.response) {
                return result;
            } else {
                throw new Error('Response does not have a valid format');
            }
        } catch (error) {
            console.error(error);
            throw error;
        }
    }
}

export default AuctionService;

// Example usage:
const result = await AuctionService.export({ resource: 'someResource' });