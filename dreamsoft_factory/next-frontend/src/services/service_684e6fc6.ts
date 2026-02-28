import api from '@/lib/api';

class OfferService {
  static async deleteUserResource(resource: string, id: number): Promise<any> {
    try {
      const response = await api.delete(`${process.env.API_URL}/${[resource, id].join('/')}`);
      if (response.data.response) {
        // Assuming cache.remove is a method to clear the cache
        cache.remove('collection');
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      throw error;
    }
  }

  static async userCanAddFile(): Promise<any> {
    try {
      const response = await api.get(`${process.env.API_URL}/offerItems/userCanAddFile`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  static async toggleVisible(fileID: string, data: any): Promise<void> {
    try {
      // Assuming the endpoint requires a PUT request
      const response = await api.put(`${process.env.API_URL}/offerItems/${fileID}`, data);
      return response.data; // or whatever operation needs to be performed
    } catch (error) {
      throw error;
    }
  }
}