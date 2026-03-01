import api from '@/lib/api';

class VolumeService {
  private resource: string;

  constructor(resource: string) {
    this.resource = resource;
  }

  public async getRtDetails(volume: string): Promise<any> {
    const resource = `${this.resource}/${volume}/ps_rt_details`;
    
    try {
      return await api.get(resource);
    } catch (error) {
      throw error;
    }
  }

  public async saveRtDetails(volume: string, item: any): Promise<any> {
    const resource = `${this.resource}/${volume}/ps_rt_details`;

    try {
      const response = await api.patch(resource, item);

      if (response.response) {
        return response;
      } else {
        throw new Error('Response not as expected');
      }
    } catch (error) {
      throw error;
    }
  }
}