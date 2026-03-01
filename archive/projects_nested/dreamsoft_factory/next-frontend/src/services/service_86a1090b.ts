import axios, { AxiosResponse } from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class DpOrderService {

  private apiUrl: string;

  constructor(apiUrl: string) {
    this.apiUrl = apiUrl;
  }

  async changeMultiOffer(resource: string, data: any): Promise<AxiosResponse> {
    try {
      const response = await axios.post(this.apiUrl + '/' + resource + '/changeMultiOffer', data);
      if (response.data.response) {
        return response;
      } else {
        throw new Error('No response');
      }
    } catch (error: any) {
      throw error;
    }
  }

}

export default DpOrderService;

// Usage example in a Next.js API route
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const dpOrderService = new DpOrderService(process.env.API_URL);
  
  try {
    const response = await dpOrderService.changeMultiOffer('your-resource', { /* your data */ });
    res.status(200).json(response.data);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
}