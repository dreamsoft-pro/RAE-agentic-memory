import api from '@/lib/api';

class PsWorkspaceService {

    static async getByPrintType(printTypeID: string): Promise<any> {
        const url = `/ps_workspaces/getByPrintType/${printTypeID}`;
        try {
            const data = await api.get(url);
            return data;
        } catch (error) {
            throw error;
        }
    }

    static async devices(workspaceId: number): Promise<any> {
        const url = `${process.env.API_URL}/ps_workspaces/${workspaceId}/ps_workspaceDevices`;
        try {
            const response = await api.get(url);
            return response.data;
        } catch (error) {
            throw error;
        }
    }

    static async setDevices(workspace: any, devices: any[]): Promise<any> {
        const url = `${process.env.API_URL}/ps_workspaces/${workspace.ID}/ps_workspaceDevices`;
        try {
            const response = await api.put(url, { devices });
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default PsWorkspaceService;