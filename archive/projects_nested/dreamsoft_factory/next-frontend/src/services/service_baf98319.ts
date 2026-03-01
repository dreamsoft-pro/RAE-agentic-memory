import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class DpOrderService {
    private apiUrl: string;

    constructor(apiUrl: string) {
        this.apiUrl = apiUrl;
    }

    updatePrice() {
        return axios.patch(`${this.apiUrl}/updatePrice`);
    }

    recalculateDelivery(params: any) {
        return axios.patch(`${this.apiUrl}/recalculateDelivery`, params);
    }
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
    const dpOrderService = new DpOrderService(process.env.API_URL);

    if (req.method === 'PATCH' && req.url?.includes('/updatePrice')) {
        try {
            const response = await dpOrderService.updatePrice();
            res.status(200).json(response.data);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    if (req.method === 'PATCH' && req.url?.includes('/recalculateDelivery')) {
        try {
            const response = await dpOrderService.recalculateDelivery(req.body);
            res.status(200).json(response.data);
        } catch (error) {
            res.status(500).json({ error: error.message });
        }
    }

    // Add more cases for different URLs and methods as needed.
}