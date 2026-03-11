import api from '@/lib/api';

class UserTypeService {

  static async deleteUserType(id: string): Promise<any> {
    try {
      const response = await api.delete(`/userTypes/${id}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  static async getTypeRoles(typeId: string): Promise<any[]> {
    try {
      const resource = ['userTypes', 'userTypeRoles', typeId].join('/');
      const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
      const response = await api.get(url);
      if (response.data.response) {
        return response.data.items;
      } else {
        throw new Error('Invalid response');
      }
    } catch (error) {
      throw error;
    }
  }

  static async setTypeRoles(typeId: string, items: any[]): Promise<any> {
    try {
      const resource = ['userTypes', 'userTypeRoles', typeId].join('/');
      const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;
      const response = await api.put(url, { items });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

}

export default UserTypeService;