import axios, { AxiosResponse } from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class DpOrderService {
    private static API_URL: string;

    public static initialize(apiUrl: string) {
        this.API_URL = apiUrl;
    }

    public static edit(id: number | string, data: any): Promise<AxiosResponse> {
        return axios.put(`${this.API_URL}/${resource}/${id}`, data);
    }

    public static sellerNotReady(): Promise<AxiosResponse> {
        return axios.get(`${this.API_URL}/${resource}/sellerNotReady`);
    }
    
    // Assuming `getCart` needs to be implemented as a server-side API route in Next.js.
    // This is how you would implement the getCart method as an API route handler.

    public static async getCart(req: NextApiRequest, res: NextApiResponse) {
        try {
            const response = await axios.get(`${this.API_URL}/cart`);
            res.status(200).json(response.data);
        } catch (error) {
            res.status(500).json({ message: 'Error fetching cart data' });
        }
    }
}

// Usage example:
DpOrderService.initialize('https://api.example.com');

export default DpOrderService;