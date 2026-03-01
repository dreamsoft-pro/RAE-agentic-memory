import api from '@/lib/api';

class UserTypeService {
  static async setType(type: { ID: string }, items: any[]): Promise<any> {
    const resource = ['userTypes', 'userTypeRoles', type.ID].join('/');
    
    try {
      const response = await api.post(`${process.env.API_URL}/${resource}`, items);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  static async getTypeGroups(type: { ID: string }): Promise<any[]> {
    const resource = ['userTypes', 'userTypeGroups', type.ID].join('/');
    
    try {
      const response = await api.get(`${process.env.API_URL}/${resource}`);
      return response.data.response ? response.data.items : [];
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  static async setTypeGroups(type: { ID: string }, items: any[]): Promise<any> {
    const resource = ['userTypes', 'userTypeGroups', type.ID].join('/');
    
    try {
      const response = await api.post(`${process.env.API_URL}/${resource}`, items);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }
}

export default UserTypeService;