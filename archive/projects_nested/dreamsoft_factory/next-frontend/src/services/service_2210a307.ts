import api from '@/lib/api';

class ViewService {
  private routeID: string;

  constructor(routeID: string) {
    this.routeID = routeID;
  }

  private getResource(): string {
    // Implement the logic for getting resource here
    return 'your-resource-name';
  }

  public async update(data: any): Promise<any> {
    const resource = this.getResource();
    try {
      const response = await api.put(`${process.env.API_URL}/${resource}/?routeID=${this.routeID}`, data);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      throw error;
    }
  }

  public async remove(dataID: string): Promise<any> {
    const resource = this.getResource();
    try {
      const response = await api.delete(`${process.env.API_URL}/${resource}/${dataID}`);
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

export default ViewService;