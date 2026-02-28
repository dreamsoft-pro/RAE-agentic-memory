import axios, { AxiosPromise } from 'axios';
import { Cache } from './cache'; // Adjust the import path as necessary

class ComplexService {
  private apiUrl: string;

  constructor(config: { API_URL: string }) {
    this.apiUrl = config.API_URL;
  }

  public async postRelatedFormat(baseFormatID: number, formats: any[]): AxiosPromise<any> {
    try {
      const response = await axios.post(`${this.apiUrl}/${baseFormatID}/relatedFormat`, { formats });
      if (response.data.response) {
        Cache.remove('resource'); // Adjust 'resource' to the actual key used in cache
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      throw error;
    }
  }
}

export default ComplexService;