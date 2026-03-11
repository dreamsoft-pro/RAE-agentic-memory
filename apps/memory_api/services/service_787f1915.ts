import api from '@/lib/api';
import { Cache } from '@/path/to/cache'; // Assuming cache is defined somewhere in your project

export default class VolumeService {
  private resource: string;
  private url: string;

  constructor(resource: string) {
    this.resource = resource;
    this.url = `${api}/volumes`; // Adjust the URL based on your API endpoint
  }

  async add(item: any): Promise<any> {
    try {
      const response = await api.post(`${this.url}`, item);
      if (response.data.ID) {
        Cache.remove(this.resource); // Remove cache after adding an item
        return response.data;
      } else {
        throw new Error('Failed to add volume');
      }
    } catch (error) {
      throw error;
    }
  }

  async remove(item: any): Promise<any> {
    try {
      const response = await api.delete(`${this.url}/${item.ID}`);
      if (response.data.response) {
        Cache.remove(this.resource); // Remove cache after removing an item
        return response.data;
      } else {
        throw new Error('Failed to remove volume');
      }
    } catch (error) {
      throw error;
    }
  }
}