import api from '@/lib/api';

class ViewService {
  private routeID: string;

  constructor(routeID: string) {
    this.routeID = routeID;
  }

  private getResource(): string {
    // Implement your logic for getting the resource name here
    return 'your-resource-name';
  }

  async fetchMainVariables(): Promise<any> {
    const url = `${process.env.NEXT_PUBLIC_API_URL}/${this.getResource()}/mainVariables/${this.routeID}`;
    try {
      const response = await api.get(url);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  async add(data: any): Promise<any> {
    data.routeID = this.routeID;
    const resource = this.getResource();
    try {
      const url = `${process.env.NEXT_PUBLIC_API_URL}/${resource}?routeID=${this.routeID}`;
      const response = await api.post(url, data);
      if (response.data.response) {
        return response.data;
      } else {
        throw new Error('Invalid response');
      }
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  async edit(data: any): Promise<any> {
    const resource = this.getResource();
    try {
      // Implement the actual API call and logic for editing here
      return {}; // Placeholder return value, replace with actual implementation
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }
}

export default ViewService;