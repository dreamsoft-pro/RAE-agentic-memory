import api from '@/lib/api';
import { Cache } from 'tiny-invariant'; // Assuming a simple cache implementation for demonstration

class PsPriceTypeService {
  private cache: Map<string, any>;

  constructor() {
    this.cache = new Map();
  }

  async getAll(force?: boolean): Promise<any[]> {
    if (this.cache.has('collection') && !force) {
      return this.cache.get('collection');
    } else {
      try {
        const data = await api.get('/ps_pricetypes').then(response => response.data);
        const collection = data.map(item => item); // Assuming 'data' is an array of objects
        this.cache.set('collection', collection);

        if (force) {
          console.log('Emitting event with force: ', collection); // Placeholder for $rootScope.$emit
        }

        return collection;
      } catch (error) {
        throw error; // Re-throw the error to be caught by the caller
      }
    }
  }
}

export default PsPriceTypeService;