import api from '@/lib/api';

export default class GroupService {
  private async postGroupRoles(group: { ID: string }, items: any[]): Promise<any> {
    const resource = ['groups', group.ID, 'groupRoles'].join('/');
    const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}`;

    try {
      const response = await api.post(url, items);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error('Response does not have a valid structure');
      }
    } catch (error: any) {
      throw error;
    }
  }

  // If you want to expose this method publicly
  public async fetchGroupRoles = async (group: { ID: string }, items: any[]) => await this.postGroupRoles(group, items);
}