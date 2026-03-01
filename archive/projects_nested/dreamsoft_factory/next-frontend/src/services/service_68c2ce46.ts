import api from '@/lib/api';
import { RoleResponse } from '@/types'; // Assuming appropriate type definitions

class GroupService {
  static async deleteGroup(id: string): Promise<RoleResponse> {
    try {
      const response = await api.delete(`groups/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  static async getRoles(group: { ID: string }): Promise<RoleResponse[]> {
    try {
      const resource = ['groups', group.ID, 'groupRoles'].join('/');
      const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
      const response = await api.get(url);
      if (response.data.response) {
        return response.data.items;
      } else {
        throw new Error('Failed to retrieve roles');
      }
    } catch (error) {
      throw error;
    }
  }

  static async setRoles(group: { ID: string }, items: RoleResponse[]): Promise<RoleResponse> {
    try {
      const resource = ['groups', group.ID, 'groupRoles'].join('/');
      const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
      const response = await api.put(url, { items });
      return response.data;
    } catch (error) {
      throw error;
    }
  }
}

export default GroupService;