import { NextApiRequest, NextApiResponse } from 'next';
import axios from '@/lib/api';

class CategoryDescriptionsService {
    private resource: string;

    constructor(resource: string) {
        this.resource = resource;
    }

    async update(data: any): Promise<any> {
        try {
            const response = await axios.put(`${process.env.API_URL}${this.resource}`, data);
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }

    getDescription(data: any): Promise<any> {
        return this.request('GET', data);
    }

    sort(data: any): Promise<any> {
        return this.request('PUT', data);
    }

    private async request(method: string, data: any): Promise<any> {
        try {
            const response = await axios({
                method,
                url: `${process.env.API_URL}${this.resource}`,
                data
            });
            return response.data;
        } catch (error) {
            throw error.response?.data || error.message;
        }
    }
}

export default CategoryDescriptionsService;

// Example usage in a Next.js API route:
export default function handler(req: NextApiRequest, res: NextApiResponse) {
    const service = new CategoryDescriptionsService('your-resource');
    
    switch (req.method) {
        case 'PUT':
            return service.update(req.body).then(data => res.json(data)).catch(error => res.status(500).json({ error }));
        case 'GET':
            return service.getDescription(req.query).then(data => res.json(data)).catch(error => res.status(500).json({ error }));
        default:
            res.setHeader('Allow', ['PUT', 'GET']);
            res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}