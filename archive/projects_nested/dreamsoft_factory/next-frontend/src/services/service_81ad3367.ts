import api from '@/lib/api';

class ProcessService {
  private cache: any; // Replace 'any' with appropriate type if known

  constructor(cache: any) {
    this.cache = cache;
  }

  async sortResource(resource: string, sort: any): Promise<any> {
    try {
      const response = await api.patch(`${process.env.API_URL}/${resource}/sort`, sort);
      if (response.data.response) {
        this.cache.remove('collection');
        return response.data;
      } else {
        throw new Error('Response error');
      }
    } catch (error) {
      console.error(error); // or handle error properly
      throw error; // re-throw to reject the promise
    }
  }
}

export default ProcessService;