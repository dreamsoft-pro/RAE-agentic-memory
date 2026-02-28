import api from '@/lib/api';

class SkillService {
  private cache: any; // Adjust type as needed

  constructor() {
    this.cache = {}; // Example initialization, adjust as necessary
  }

  async deleteResource(resource: string, id: number): Promise<any> {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}/${id}`;
    try {
      const response = await api.delete(url);
      if (response.data.response) {
        this.cache.remove('collection');
        return response.data;
      } else {
        throw new Error('Resource deletion failed');
      }
    } catch (error: any) {
      throw error;
    }
  }

  // Other methods can go here
}

export default SkillService;