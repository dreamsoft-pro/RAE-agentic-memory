import api from '@/lib/api';
import { Cache } from 'memory-cache';

class OrderService {
  private resource: string;
  private cache: Cache;
  private getAllDef: Promise<unknown> | null;

  constructor() {
    this.resource = 'orders';
    this.cache = new Cache();
    this.getAllDef = null;
  }

  async getAll(force?: boolean): Promise<any[]> {
    if (!this.getAllDef || force) {
      this.getAllDef = api.get(this.resource).then((response: any) => response.data);
    }
    
    if (force || !this.cache.get('collection')) {
      const data = await this.getAllDef;
      this.cache.put('collection', data, null);
      return data;
    } else {
      return this.cache.get('collection');
    }
  }

  async ongoing(orderID: string): Promise<any> {
    // Assuming you have a specific URL for order ongoing
    const response = await api.get(`${this.resource}/${orderID}/ongoings`);
    return response.data;
  }
}

export default OrderService;