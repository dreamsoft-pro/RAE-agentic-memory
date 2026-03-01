import api from '@/lib/api';
import { NextApiRequest } from 'next';

class OrderService {
  static async accept(orderID: string, accept: boolean): Promise<any> {
    try {
      const response = await api.patch(`${process.env.API_URL}/${resource}/${orderID}`, { accept });
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error('Failed to accept order');
      }
    } catch (error) {
      throw error;
    }
  }

  static async noAccept(orderID: string, acceptInfo: any, acceptFiles: any): Promise<any> {
    try {
      const response = await api.patch(`${process.env.API_URL}/${resource}/${orderID}`, { accept: -1, acceptInfo, acceptFiles });
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error('Failed to reject order');
      }
    } catch (error) {
      throw error;
    }
  }

  // Make sure `resource` is defined somewhere in your class or passed as a parameter
}

export default OrderService;