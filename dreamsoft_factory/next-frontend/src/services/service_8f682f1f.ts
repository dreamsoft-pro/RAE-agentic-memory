import api from '@/lib/api';

class PrintTypeService {

  private getResource(): string {
    // Implementation of this method should be provided based on your use case
    return 'resourceName'; // Replace with actual resource name
  }

  public async doPost(item: any): Promise<any> {
    const resource = this.getResource();
    try {
      const response = await api.post(resource, item);
      if (response.data.ID) {
        cache.remove(resource); // Assuming cache is defined elsewhere in your application
        return response.data;
      } else {
        throw new Error('Data does not contain ID');
      }
    } catch (error) {
      throw error; // Re-throw the caught error
    }
  }

  public async edit(item: any): Promise<any> {
    const resource = this.getResource();
    try {
      const response = await api.put(resource, item);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error('Data does not contain response');
      }
    } catch (error) {
      throw error; // Re-throw the caught error
    }
  }

}

// Usage example:
const service = new PrintTypeService();
service.doPost({ /* item data */ })
  .then(data => console.log(data))
  .catch(error => console.error(error));

service.edit({ /* item data */ })
  .then(data => console.log(data))
  .catch(error => console.error(error));