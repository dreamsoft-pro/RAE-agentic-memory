import api from '@/lib/api';

export default class RouteService {
  static async level(state: string): Promise<any> {
    try {
      const response = await api.get(`${resource}/level/${state}`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  static async patchResource(elem: any, resource: string): Promise<any> {
    try {
      const response = await api.patch(`${resource}/${elem.ID}`, elem);
      if (response?.data?.response) {
        return response.data;
      } else {
        throw new Error('Response data is not valid');
      }
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  // Ensure the 'resource' variable is defined before use.
}