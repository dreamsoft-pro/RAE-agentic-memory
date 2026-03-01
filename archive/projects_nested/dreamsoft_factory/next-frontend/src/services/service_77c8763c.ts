import api from '@/lib/api';

class CalculateDataService {
    private readonly apiUrl: string;

    constructor() {
        this.apiUrl = process.env.NEXT_PUBLIC_API_URL + ['calculate', 'printOffer'].join('/');
    }

    public async calculateAndPrintOffer(data: any): Promise<any> {
        try {
            const response = await api.patch(this.apiUrl, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }
}

export default new CalculateDataService();