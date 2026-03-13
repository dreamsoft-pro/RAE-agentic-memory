import api from '@/lib/api';

interface Cache {
  remove(key: string): void;
}

const cache: Cache = {
  // Implement actual caching logic here or use an existing caching service.
};

class OfferService {

  private static async postData<T>(url: string, data: any): Promise<T> {
    try {
      const response = await api.post(url, data);
      return response.data as T;
    } catch (error) {
      throw error.response?.data ?? new Error('An unknown error occurred');
    }
  }

  private static async putData<T>(url: string, data: any): Promise<T> {
    try {
      const response = await api.put(url, data);
      return response.data as T;
    } catch (error) {
      throw error.response?.data ?? new Error('An unknown error occurred');
    }
  }

  public static async create(resource: string, data: any): Promise<any> {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
    try {
      const result = await OfferService.postData(url, data);
      if ('ID' in result) {
        cache.remove('collection');
        return result;
      } else {
        throw new Error(`Unexpected response format: ${JSON.stringify(result)}`);
      }
    } catch (error) {
      throw error;
    }
  }

  public static async update(resource: string, offer: any): Promise<any> {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
    try {
      const result = await OfferService.putData(url, offer);
      if ('response' in result) {
        cache.remove('collection');
        return result;
      } else {
        throw new Error(`Unexpected response format: ${JSON.stringify(result)}`);
      }
    } catch (error) {
      throw error;
    }
  }

  public static async remove(resource: string, id: number): Promise<void> {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/${id}`;
    try {
      await api.delete(url);
      cache.remove('collection');
    } catch (error) {
      throw new Error(`Failed to delete resource ${url}: ${error.message}`);
    }
  }

}

export default OfferService;