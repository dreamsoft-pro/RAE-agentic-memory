import api from '@/lib/api';

class TypeService {
  static async getOneByID(groupID: string | number, typeID: string | number): Promise<any> {
    try {
      const response = await api.get(`ps_groups/${groupID}/ps_types/oneByID/${typeID}`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error; // Handle both errors from the server and network issues
    }
  }

  static cacheRemove(groupID: string | number): void {
    // Assuming 'cache' is defined elsewhere in your application.
    cache.remove(`collection${groupID}`);
  }
}

export default TypeService;