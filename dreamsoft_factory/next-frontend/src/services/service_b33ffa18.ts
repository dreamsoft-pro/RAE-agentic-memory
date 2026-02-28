import api from '@/lib/api';

class OperationService {
    static async getProcesses(operation: { ID: string }, resource: string): Promise<any> {
        const url = `${process.env.API_URL}/${[resource, operation.ID, 'operationProcesses'].join('/')}`;
        
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }

    static async setProcesses(operation: { ID: string }, processes: any[], resource: string): Promise<any> {
        const url = `${process.env.API_URL}/${[resource, operation.ID, 'operationProcesses'].join('/')}`;

        try {
            const response = await api.post(url, processes);
            return response.data;
        } catch (error) {
            throw error.response ? error.response : error;
        }
    }
}