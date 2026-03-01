import api from "@/lib/api";

class OngoingService {

    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async getOperationsLogs(dates: any): Promise<any> {
        try {
            const response = await api.post(`${this.resource}/getOperationsLogs`, dates);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    public async getOngoingsForCalcProduct(calcProductId: string): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/ongoingsForCalcProduct/${calcProductId}`);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

}

export default OngoingService;