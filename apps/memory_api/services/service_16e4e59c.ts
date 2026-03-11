import api from '@/lib/api';

class StaticPrice {
  private resource: string = 'static_price'; // Example default value for demonstration

  public async export(): Promise<any> {
    try {
      const response = await api.get(`${this.resource}/export`);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error('Response did not contain expected data structure');
      }
    } catch (error: any) {
      console.error(error);
      throw error;
    }
  }

  constructor(resource?: string) {
    if (resource) {
      this.resource = resource;
    }
  }
}

export default StaticPrice;