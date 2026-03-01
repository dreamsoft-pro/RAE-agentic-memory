import api from '@/lib/api';

export default class UserTypeService {
  private resource: string;

  constructor() {
    this.resource = 'userTypes';
  }

  public async getAll(): Promise<any[]> {
    try {
      const response = await api.get(this.resource);
      return response.data;
    } catch (error) {
      throw new Error('Failed to fetch user types');
    }
  }

  public async create(type: any): Promise<any> {
    try {
      const response = await api.post(this.resource, type);
      return response.data;
    } catch (error) {
      throw new Error('Failed to create user type');
    }
  }

  public async update(type: any): Promise<any> {
    try {
      const response = await api.put(`${this.resource}/${type.id}`, type);
      if (response.status === 200) {
        return response.data;
      } else {
        throw new Error('Failed to update user type');
      }
    } catch (error) {
      throw new Error('Failed to update user type');
    }
  }

  public async remove(id: number): Promise<void> {
    try {
      await api.delete(`${this.resource}/${id}`);
    } catch (error) {
      throw new Error('Failed to delete user type');
    }
  }
}