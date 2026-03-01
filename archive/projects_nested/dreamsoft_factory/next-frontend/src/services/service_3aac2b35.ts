import { AxiosInstance } from 'axios';
import axios from 'axios';

interface ConfigType {
  API_URL: string;
}

export default class DpOrderService {
  private apiClient: AxiosInstance;

  constructor(private config: ConfigType) {
    this.apiClient = axios.create({
      baseURL: config.API_URL,
    });
  }

  async getAll(): Promise<any[]> {
    try {
      const response = await this.apiClient.get('dp_orders');
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : error;
    }
  }

  async get(id: string): Promise<any> {
    try {
      const response = await this.apiClient.get(`dp_orders/${id}`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : error;
    }
  }
}