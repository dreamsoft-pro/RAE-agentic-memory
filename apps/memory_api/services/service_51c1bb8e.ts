import api from "@/lib/api";

class OngoingService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async getAllDeviceLogs(dates: any): Promise<any> {
        try {
            const response = await api.post(`${this.resource}/getAllDeviceLogs`, dates);
            return response.data;
        } catch (error) {
            throw new Error(error.response ? error.response.data : error.message);
        }
    }

    public async getOrderLogs(orderID: string, dates: any): Promise<any> {
        try {
            const response = await api.post(`${this.resource}/getOrderLogs/${orderID}`, dates);
            return response.data;
        } catch (error) {
            throw new Error(error.response ? error.response.data : error.message);
        }
    }
}