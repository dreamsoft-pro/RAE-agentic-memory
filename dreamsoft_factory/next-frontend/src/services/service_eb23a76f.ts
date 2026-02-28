import api from "@/lib/api";

class OngoingService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    public async getFinishedByOperator(operatorID: number): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/finishedByOperator/${operatorID}`);
            return response.data;
        } catch (error) {
            throw error.response?.data ?? new Error('Failed to fetch data');
        }
    }

    public async getOperatorLogs(operatorID: number, dates: any): Promise<any> {
        try {
            const response = await api.post(`${this.resource}/getOperatorLogs/${operatorID}`, dates);
            return response.data;
        } catch (error) {
            throw error.response?.data ?? new Error('Failed to fetch data');
        }
    }
}

export default OngoingService;