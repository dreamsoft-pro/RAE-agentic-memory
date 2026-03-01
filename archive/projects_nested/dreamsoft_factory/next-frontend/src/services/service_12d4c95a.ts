import { NextApiRequest, NextApiResponse } from 'next';
import axios, { AxiosPromise } from 'axios';

class CountriesService {
  private API_URL: string = process.env.NEXT_PUBLIC_API_URL as string; // Assume you have this environment variable set

  getResource(): string {
    return 'dp_countries';
  }

  getAll(): AxiosPromise<any> {
    const resource = this.getResource();
    return axios.get(`${this.API_URL}/${resource}`);
  }
}

// Example usage in a Next.js API route
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  const countriesService = new CountriesService();

  try {
    const response = await countriesService.getAll();
    res.status(200).json(response.data);
  } catch (error) {
    res.status(error.response?.status || 500).json({ message: error.message });
  }
}