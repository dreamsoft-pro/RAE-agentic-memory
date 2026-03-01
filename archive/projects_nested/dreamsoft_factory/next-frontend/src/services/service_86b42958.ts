import api from '@/lib/api';

export class SkillService {
  private static async getDevices(skill: { ID: string }, resource: string): Promise<any> {
    try {
      const url = `${process.env.API_URL}/${[resource, skill.ID, 'skillDevices'].join('/')}`;
      const response = await api.get(url);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  private static async setDevices(skill: { ID: string }, devices: any[], resource: string): Promise<any> {
    try {
      const url = `${process.env.API_URL}/${[resource, skill.ID, 'skillDevices'].join('/')}`;
      const response = await api.patch(url, devices);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error('Response data does not contain expected structure');
      }
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  private static async create(data: any[], resource: string): Promise<any> {
    try {
      const url = `${process.env.API_URL}/${resource}`;
      const response = await api.post(url, data);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  // Example usage of the methods:
  static async exampleUsage(skill: { ID: string }, devices: any[], resource: string): Promise<void> {
    try {
      const getResponse = await SkillService.getDevices(skill, resource);
      console.log('GET Response:', getResponse);

      const setResponse = await SkillService.setDevices(skill, devices, resource);
      console.log('PATCH Response:', setResponse);

      // The create method usage would be similar with the appropriate data and resource
    } catch (error) {
      console.error('Error occurred:', error.message);
    }
  }
}