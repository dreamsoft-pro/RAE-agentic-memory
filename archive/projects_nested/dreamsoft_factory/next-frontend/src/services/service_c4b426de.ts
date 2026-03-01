import api from '@/lib/api';

class OperatorService {
  static async deleteOperator(resource: string, id: number) {
    try {
      const response = await api.delete(`${resource}/${id}`);
      cache.remove('collection');
      return response.data;
    } catch (error) {
      throw error.response ? error : new Error(JSON.stringify(error));
    }
  }

  static async getSkills(operator: { ID: string }) {
    try {
      const response = await api.get(`${resource}/${operator.ID}/operatorSkills`);
      return response.data;
    } catch (error) {
      throw new Error(JSON.stringify(error));
    }
  }

  static async setSkills(operator: { ID: string }, skills: any[]) {
    const url = `${resource}/${operator.ID}/operatorSkills`;
    try {
      await api.put(url, { skills });
    } catch (error) {
      throw new Error(JSON.stringify(error));
    }
  }
}

// Ensure 'resource' is defined before using it
const resource = 'your-resource-name'; // Replace with actual resource name

export default OperatorService;