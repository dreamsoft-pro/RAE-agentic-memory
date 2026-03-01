import axios from 'axios';
import { NextApiRequest, NextApiResponse } from 'next';

class CouponService {
  private apiUrl: string;

  constructor(config: { API_URL: string }) {
    this.apiUrl = config.API_URL;
  }

  getResource(): string[] {
    return ['dp_coupons'];
  }

  async check(coupon: string, orderID: string): Promise<any> {
    const resource = this.getResource();
    resource.push('check');

    try {
      const response = await axios.post(`${this.apiUrl}/${resource.join('/')}`, {
        coupon,
        orderID
      });
      return response.data;
    } catch (error) {
      throw error.response ? error.response.data : error;
    }
  }
}

export default CouponService;