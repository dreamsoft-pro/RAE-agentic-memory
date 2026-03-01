import api from '@/lib/api';

class PsPrintTypeWorkspaceService {
    private resource: string = 'ps_printTypeWorkspaces';

    public async getAll(printTypeID: number, formatID: number): Promise<any> {
        try {
            const response = await api.get(`${this.resource}/${printTypeID}?formatID=${formatID}`);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default PsPrintTypeWorkspaceService;