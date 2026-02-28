import api from "@/lib/api";

class AuctionService {
    private apiUrl: string;

    constructor() {
        this.apiUrl = process.env.API_URL || "";
    }

    public async exportData(resource: string, params?: Record<string, any>): Promise<any> {
        try {
            const response = await api.get(`${this.apiUrl}/${resource}/export`, { params });
            if (response.data.response) {
                response.data.apiUrl = this.apiUrl;
                return response.data;
            } else {
                throw new Error('Invalid data response');
            }
        } catch (error: any) {
            throw error;
        }
    }
}

export default AuctionService;