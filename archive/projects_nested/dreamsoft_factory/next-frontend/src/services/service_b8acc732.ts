import api from '@/lib/api';

class AuctionService {

    private async postSelectWinner(resource: string, auctionID: number, responseID: number): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${[resource, auctionID, 'auctionSelectWinner'].join('/')}`;
            const response = await api.post(url, { responseID });
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async responseWinner(resource: string, auctionID: number): Promise<any> {
        try {
            const url = `${process.env.API_URL}/${[resource, 'responseWinner', auctionID].join('/')}`;
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    public async finishAuction(auctionID: number): Promise<any> {
        try {
            // Assuming you need to perform some action here.
            const url = `${process.env.API_URL}/some/finish/auction/${auctionID}`;
            const response = await api.post(url, {}); // Modify this as needed
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

}

export default new AuctionService();