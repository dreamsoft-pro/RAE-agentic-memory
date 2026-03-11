import api from '@/lib/api';
import { Cache } from 'next/cache';

interface ServiceCache {
  [key: string]: any;
}

class PrintTypeService {
  private cache: ServiceCache = {};

  getResource(): string {
    return 'ps_printtypes';
  }

  async getAll(force?: boolean): Promise<any[]> {
    const resource = this.getResource();

    if (!force && this.cache[resource]) {
      return this.cache[resource];
    }

    try {
      const response = await api.get(resource);
      this.cache[resource] = response.data.plain();
      return response.data.plain();
    } catch (error) {
      throw error;
    }
  }

  async add(item: any): Promise<any> {
    const resource = this.getResource();

    try {
      const response = await api.post(resource, item);
      // Optionally update the cache here if necessary
      this.cache[resource] = [response.data]; // Assuming a new object is returned on add
      return response.data;
    } catch (error) {
      throw error;
    }
  }
}

export default PrintTypeService;