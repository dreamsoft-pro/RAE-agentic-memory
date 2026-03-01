import api from '@/lib/api';

export default class AdminHelpService {
  private resource: string;

  constructor(resource: string) {
    this.resource = resource;
  }

  async update(module: any): Promise<any> {
    try {
      const response = await api.put(`${process.env.API_URL}/${this.resource}`, module);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      throw error;
    }
  }

  async remove(id: string): Promise<any> {
    try {
      const url = `${process.env.API_URL}/${this.resource}/${id}`;
      const response = await api.delete(url);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      throw error;
    }
  }

  async getKeys(moduleName: string): Promise<any> {
    try {
      // Assuming some logic for getting keys based on moduleName
      const url = `${process.env.API_URL}/${moduleName}/keys`; 
      const response = await api.get(url);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      throw error;
    }
  }

}