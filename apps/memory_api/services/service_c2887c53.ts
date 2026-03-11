import api from '@/lib/api';

class OrderService {

  private resource: string;

  constructor(resource: string) {
    this.resource = resource;
  }

  async getOngoingLogs(orderID: string): Promise<any> {
    try {
      const response = await api.get(`${process.env.API_URL}/${this.resource}/${orderID}/ongoings/logs`);
      return response.data;
    } catch (error) {
      throw error.response?.data || new Error('An unknown error occurred');
    }
  }

  async productCard(orderID: string): Promise<any> {
    try {
      const response = await api.get(`${process.env.API_URL}/${this.resource}/productCard/${orderID}`);
      return response.data;
    } catch (error) {
      throw error.response?.data || new Error('An unknown error occurred');
    }
  }

  async accept(orderID: string, accept: boolean): Promise<any> {
    try {
      const response = await api.post(`${process.env.API_URL}/${this.resource}/accept/${orderID}`, { accept });
      return response.data;
    } catch (error) {
      throw error.response?.data || new Error('An unknown error occurred');
    }
  }

}

export default OrderService;