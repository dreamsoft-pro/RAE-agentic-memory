import api from '@/lib/api';

class ReclamationFaultService {

    private resource: string = 'dp_reclamation_faults';
    
    public async getFaults(): Promise<any> {
        try {
            const response = await api.get(this.resource);
            return response.data;
        } catch (error) {
            throw new Error(error.message);
        }
    }

    public async addFault(data: any): Promise<any> {
        try {
            const response = await api.post(this.resource, data);
            return response.data;
        } catch (error) {
            throw new Error(error.message);
        }
    }
}

export default ReclamationFaultService;