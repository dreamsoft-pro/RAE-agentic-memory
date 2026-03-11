import api from '@/lib/api';

class RoleService {
  private baseUrl = '/roles'; // Assuming this is relative to your API setup

  public async create(group: any): Promise<any> {
    try {
      const response = await api.post(this.baseUrl, group);
      return response.data;
    } catch (error) {
      throw error; // Rethrow if the request fails
    }
  }

  public async update(group: any): Promise<any> {
    try {
      const response = await api.put(`${this.baseUrl}/${group.id}`, group); // Assuming group has an id field for PUT requests
      return response.data;
    } catch (error) {
      throw error; // Rethrow if the request fails
    }
  }

  public async remove(id: string | number): Promise<any> {
    try {
      const response = await api.delete(`${this.baseUrl}/${id}`);
      return response.data;
    } catch (error) {
      throw error; // Rethrow if the request fails
    }
  }
}

export default new RoleService();