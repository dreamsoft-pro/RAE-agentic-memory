import api from '@/lib/api';

class GroupService {
  private resource: string;

  constructor() {
    this.resource = 'groups';
  }

  async getAll(): Promise<any[]> {
    try {
      const response = await api.get(this.resource);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async create(group: any): Promise<any> {
    try {
      const response = await api.post(this.resource, group);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  async update(id: string | number, group: any): Promise<any> {
    const url = `${this.resource}/${id}`;
    try {
      const response = await api.put(url, group);
      if ('response' in response.data && response.data.response) {
        return response.data;
      } else {
        throw new Error('Update failed');
      }
    } catch (error) {
      throw error;
    }
  }

  async remove(id: string | number): Promise<void> {
    const url = `${this.resource}/${id}`;
    try {
      await api.delete(url);
    } catch (error) {
      throw error;
    }
  }
}

export default GroupService;