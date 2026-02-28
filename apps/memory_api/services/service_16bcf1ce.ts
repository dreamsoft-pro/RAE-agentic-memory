import api from '@/lib/api';
import { Cache } from 'your-cache-module'; // Assuming some cache module for TypeScript

interface PageServiceProps {
  resource: string;
  typeID?: number; // This is optional as per the given code snippet
}

class PageService {
  private readonly cache: Cache;
  private force: boolean;

  constructor(cache: Cache, force = false) {
    this.cache = cache;
    this.force = force;
  }

  async getResource(resource: string): Promise<any> {
    if (this.cache.get(resource) && !this.force) {
      return this.cache.get(resource);
    } else {
      try {
        const response = await api.restangular.all(`/${resource}`).getList();
        this.cache.put(resource, response.plain());
        return response.plain();
      } catch (error) {
        throw error;
      }
    }
  }

  async getCustomNames(resource: string, typeID?: number): Promise<any> {
    try {
      const response = await api.restangular.all(`/${resource}`).one('customName', typeID).get();
      return response.plain();
    } catch (error) {
      throw error;
    }
  }
}

export default PageService;