import axios from 'axios';
import { Config } from '@/config'; // Adjust the import path as necessary

class PaymentService {
  private API_URL: string = Config.API_URL; // Assuming Config contains your API_URL

  async getPaymentData(resource: string[]): Promise<any> {
    try {
      const response = await axios.get(this.API_URL + resource.join('/'));
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }
}

export default PaymentService;