import api from "@/lib/api";

class AuctionService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async getForCompany(filters?: any): Promise<any> {
        let url = [this.resource, 'forCompany'].join('/');
        
        if (filters && Object.keys(filters).length > 0) {
            const qs = new URLSearchParams(filters as Record<string, string>).toString();
            url += '?' + qs;
        }

        try {
            return await api.get(url);
        } catch (error) {
            throw error;
        }
    }

    async response(auctionID: number): Promise<any> {
        let url = [this.resource, auctionID.toString(), 'auctionResponses'].join('/');
        
        try {
            return await api.get(url);
        } catch (error) {
            throw error;
        }
    }
}

export default AuctionService;