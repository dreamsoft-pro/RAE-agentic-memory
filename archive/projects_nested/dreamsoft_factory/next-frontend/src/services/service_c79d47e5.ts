import api from '@/lib/api';

class CalculationService {
    private groupID: string;
    private typeID: string;

    constructor(groupID: string, typeID: string) {
        this.groupID = groupID;
        this.typeID = typeID;
    }

    async updateName(data: any): Promise<any> {
        const resource = ['ps_groups', this.groupID, 'ps_types', this.typeID, 'ps_calculate', 'updateName', data.productID].join('/');
        
        try {
            const response = await api.patch(`${process.env.API_URL}/${resource}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }

    async performAction(data: any): Promise<any> {
        const resource = ['ps_groups', this.groupID, 'ps_types', this.typeID].join('/');
        
        try {
            const response = await api.post(`${process.env.API_URL}/${resource}`, data);
            return response.data;
        } catch (error) {
            throw error.response ? error.response.data : error;
        }
    }
}

export default CalculationService;