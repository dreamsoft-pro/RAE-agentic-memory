import api from '@/lib/api';

class MailContentService {
  private getResource(): string {
    // Your implementation for getting resource path
    return 'your-resource-path';
  }

  public async add(item: any): Promise<any> {
    const resource = this.getResource();
    try {
      const response = await api.post(`${process.env.API_URL}${resource}`, item);
      if (response.data.response) {
        // Cache removal logic here, assuming you have a cache service
        // cache.remove(resource);

        return response.data;
      } else {
        throw new Error('Response does not contain required data');
      }
    } catch (error) {
      throw error;
    }
  }

  public async edit(item: any): Promise<any> {
    const resource = this.getResource();
    try {
      const response = await api.put(`${process.env.API_URL}${resource}`, item);
      if (response.data.response) {
        // Cache removal logic here
        // cache.remove(resource);

        return response.data;
      } else {
        throw new Error('Response does not contain required data');
      }
    } catch (error) {
      throw error;
    }
  }
}

export default MailContentService;