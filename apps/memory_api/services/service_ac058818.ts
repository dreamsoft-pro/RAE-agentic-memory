import api from '@/lib/api';

class ViewService {
  private routeID: string;
  private viewID: string;

  constructor(routeID: string, viewID: string) {
    this.routeID = routeID;
    this.viewID = viewID;
  }

  getResource(): string {
    return 'dp_views';
  }

  async getAll() {
    const resource = this.getResource();
    try {
      const response = await api.get(`${resource}?routeID=${this.routeID}`);
      return response.data;
    } catch (error) {
      throw new Error(error);
    }
  }

  async makeViewReplace(replaceID: string): Promise<void> {
    const resource = this.getResource();
    const data = { replaceID, routeID: this.routeID };
    
    // The implementation of `makeViewReplace` function needs to be completed based on requirements.
    try {
      await api.post(`${resource}/replace`, data);
    } catch (error) {
      throw new Error(error);
    }
  }
}

export default ViewService;