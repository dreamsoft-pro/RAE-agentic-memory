import axios, { AxiosResponse } from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';
import api from '@/lib/api';

class PsWorkspaceService {
    private resource: string;
    private url: string;

    constructor(private workspaceId: number) {
        this.resource = ['ps_workspaces', `${workspaceId}`, 'ps_workspaceDevices'].join('/');
        this.url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`;
    }

    public async updateDevices(devices: any): Promise<AxiosResponse> {
        try {
            const response = await api.patch(this.url, devices);
            if (response.data.response) {
                return response;
            } else {
                throw new Error('Failed to update devices');
            }
        } catch (error) {
            throw error;
        }
    }

    public static async handleApiRequest(req: NextApiRequest, res: NextApiResponse): Promise<void> {
        try {
            const workspaceId = Number.parseInt(req.query.workspaceId as string);
            if (!isNaN(workspaceId)) {
                const service = new PsWorkspaceService(workspaceId);
                const response = await service.updateDevices(req.body);
                res.status(200).json(response.data);
            } else {
                res.status(400).send('Invalid workspace ID');
            }
        } catch (error) {
            console.error(error);
            res.status(500).send('Internal Server Error');
        }
    }
}

export default PsWorkspaceService;