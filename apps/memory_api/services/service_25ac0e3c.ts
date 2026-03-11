import api from '@/lib/api';

class CalculationService {
    private groupID: string;
    private typeID: string;

    constructor(groupID: string, typeID: string) {
        this.groupID = groupID;
        this.typeID = typeID;
    }

    public async calculate(data: any): Promise<any> {
        const resource = this.getResource();
        const url = `${process.env.API_URL}/${resource}`;

        try {
            const response = await api.post(url, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    public async saveCalculation(data: any): Promise<any> {
        const resource = ['ps_groups', this.groupID, 'ps_types', this.typeID, 'ps_calculate', 'saveCalculationPublic'].join('/');
        const url = `${process.env.API_URL}/${resource}`;

        try {
            const response = await api.post(url, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error.message;
        }
    }

    private getResource(): string {
        // Implement this method based on your requirements.
        // For demonstration purposes, we'll just return an empty string.
        return '';
    }
}

export default CalculationService;