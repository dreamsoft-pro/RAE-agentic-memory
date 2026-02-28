import api from '@/lib/api';

class PsConfigPaperPrice {
  private resource: string;
  private cache: any;

  constructor(resource: string, cache: any) {
    this.resource = resource;
    this.cache = cache;
  }

  public async getAll(force?: boolean): Promise<any> {
    if (this.cache.get(this.resource) && !force) {
      return this.cache.get(this.resource);
    } else {
      try {
        const response = await api.get(`${$config.API_URL}${this.resource}`);
        this.cache.put(this.resource, response.data);
        return response.data;
      } catch (error) {
        throw error;
      }
    }
  }

  public async set(paperPrice: any): Promise<any> {
    try {
      const response = await api.post(`${$config.API_URL}${this.resource}`, {
        amount: paperPrice.amount,
        expense: paperPrice.expense,
        price: paperPrice.price
      });
      if (response.data.response) {
        this.cache.remove(this.resource);
        return response.data;
      } else {
        throw new Error('Data response invalid');
      }
    } catch (error) {
      throw error;
    }
  }
}