import axios from 'axios';

const instance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL,
});

export default {
  async deleteResource(resource: string, deviceID: string, id: string): Promise<any> {
    try {
      const response = await instance.delete(`${resource}/${deviceID}/deviceSpeedChanges/${id}`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  },

  async getSideRelations(resource: string, deviceID: string): Promise<any> {
    try {
      const response = await instance.get(`${resource}/${deviceID}/deviceSideRelations`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  },
};