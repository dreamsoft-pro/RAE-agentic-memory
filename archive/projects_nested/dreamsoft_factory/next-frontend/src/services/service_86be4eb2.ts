import api from '@/lib/api';

class AuctionService {
    static async allResponses(auctionID: string): Promise<any> {
        const resource = 'auctions'; // Define the resource variable before use.
        try {
            const response = await api.get(`${process.env.API_URL}/${resource}/${auctionID}/auctionAllResponses`);
            return response.data;
        } catch (error) {
            throw error.response?.data || new Error('An unknown error occurred');
        }
    }

    static async selectWinner(auctionID: string, responseID: string): Promise<any> {
        try {
            const url = `${process.env.API_URL}/auctions/${auctionID}/selectWinner?responseId=${responseID}`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response?.data || new Error('An unknown error occurred');
        }
    }

    static async get(url: string): Promise<any> {
        try {
            const response = await api.get(`${process.env.API_URL}${url}`);
            return response.data;
        } catch (error) {
            throw error.response?.data || new Error('An unknown error occurred');
        }
    }
}

export default AuctionService;