import api from '@/lib/api';

class AuctionService {

    static async addResponse(auctionID: number, response: { realizationDate: string; description: string; items: Array<{ itemID: string; price: number; finalPrice: number }> }) {
        const resource = 'auctions'; // Define the resource variable
        const url = `${resource}/${auctionID}/auctionResponses`;

        try {
            const data = await api.post(url, response);
            if (data.response) {
                return data;
            } else {
                throw new Error('Invalid response');
            }
        } catch (error) {
            throw error; // Re-throw the error with better context
        }
    }
}