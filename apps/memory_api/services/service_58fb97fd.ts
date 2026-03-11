import api from '@/lib/api'; // Assuming this module provides Axios instance

class MailContentService {
  private getResource(): string {
    // Implementation for getting resource string
    return 'some-resource';
  }

  public async patch(item: any): Promise<any> {
    const resource = this.getResource();
    try {
      const response = await api.patch($config.API_URL + resource, item);
      if (response.data.response) {
        cache.remove(resource); // Assuming cache is a service for removing items
        return response.data;
      } else {
        throw new Error('Data rejection');
      }
    } catch (error) {
      throw error; // Rethrow the error or handle it accordingly
    }
  }

  public async remove(item: any): Promise<any> {
    const resource = this.getResource();
    try {
      await api.delete($config.API_URL + resource, { data: item });
      cache.remove(resource); // Assuming cache is a service for removing items
      return {}; // Return an empty object or handle success as needed
    } catch (error) {
      throw error; // Rethrow the error or handle it accordingly
    }
  }
}

export default MailContentService;