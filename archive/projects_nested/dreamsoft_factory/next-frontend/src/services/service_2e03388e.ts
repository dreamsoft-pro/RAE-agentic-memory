import api from '@/lib/api';

class UserTypeService {
  private async createOrUpdateUserTypeItems(type: { ID: string }, items: any[]): Promise<any> {
    const resource = ['userTypes', 'userTypeGroups', type.ID].join('/');
    
    try {
      const response = await api.post(`${process.env.API_URL}${resource}`, items);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  // Other methods can go here
}

export default UserTypeService;