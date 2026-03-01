import api from '@/lib/api';

class PermissionService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = process.env.API_URL; // Assuming API_URL is set in environment variables
  }

  async getAll(): Promise<any[]> {
    try {
      const response = await api.get(`aclPermissions`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : new Error('Error fetching data');
    }
  }

  async create(permission: any): Promise<any> {
    try {
      const response = await api.post(`aclPermissions`, permission);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : new Error('Failed to create permission');
    }
  }

  async update(permission: any): Promise<void> {
    try {
      // Assuming the resource ID is available in the 'permission' object
      const resourceId = permission.id; // Example key, adjust as needed
      await api.put(`aclPermissions/${resourceId}`, permission);
    } catch (error) {
      throw error.response ? error.response : new Error('Failed to update permission');
    }
  }

  async delete(permission: any): Promise<void> {
    try {
      const resourceId = permission.id; // Example key, adjust as needed
      await api.delete(`aclPermissions/${resourceId}`);
    } catch (error) {
      throw error.response ? error.response : new Error('Failed to delete permission');
    }
  }
}

export default PermissionService;