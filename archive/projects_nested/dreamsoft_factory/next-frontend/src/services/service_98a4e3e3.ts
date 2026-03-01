import api from '@/lib/api';

class OrderService {

  private static async patchOngoings(resource: string, orderID: number, ongoingID: number, data: any): Promise<any> {
    try {
      const response = await api.patch(`${$config.API_URL}/${resource}/${orderID}/ongoings/${ongoingID}`, data);
      if (response.data.stateChange && response.data.response) {
        return response.data;
      } else {
        throw new Error('Invalid response');
      }
    } catch (error) {
      throw error;
    }
  }

  private static async updateOngoings(resource: string, orderID: number, ongoingID: number, elem: any): Promise<any> {
    try {
      const response = await api.put(`${$config.API_URL}/${resource}/${orderID}/ongoings/${ongoingID}`, elem);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error('Invalid response');
      }
    } catch (error) {
      throw error;
    }
  }

  private static async getOngoingLogs(resource: string, orderID: number): Promise<any> {
    try {
      const response = await api.get(`${$config.API_URL}/${resource}/${orderID}/logs`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

}

export default OrderService;