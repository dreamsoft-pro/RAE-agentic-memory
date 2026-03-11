import axios from '@/lib/api';
import { Cache } from 'your-cache-module'; // Assuming you have a cache module

class OfferService {
  private static async getAll(cache: Cache, url: string, force?: boolean): Promise<any> {
    if (false && cache.get('collection') && !force) {
      return cache.get('collection');
    } else {
      try {
        const response = await axios.get($config.API_URL + url);
        cache.put('collection', response.data);
        return response.data;
      } catch (error) {
        throw error; // Ensure the error is thrown to be handled by caller
      }
    }
  }

  public static async getCurrent(resource: string): Promise<any> {
    try {
      const response = await axios.get($config.API_URL + [resource, 'getCurrent'].join('/'));
      return response.data.length === 0 ? false : response.data;
    } catch (error) {
      throw error; // Ensure the error is thrown to be handled by caller
    }
  }

  public static async addItem(item: any): Promise<any> {
    try {
      const response = await axios.post($config.API_URL + [resource, 'addItem'].join('/'), item);
      return response.data;
    } catch (error) {
      throw error; // Ensure the error is thrown to be handled by caller
    }
  }

  // Add other methods as needed following the pattern above.
}