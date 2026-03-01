import api from '@/lib/api';

class RouteService {

  private resource: string = 'your-resource-name'; // Define this as needed

  public async getOne(routeID: string): Promise<any> {
    console.log(routeID);
    try {
      const response = await api.get([this.resource, 'one', routeID].join('/'));
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  public async move(): Promise<any> {
    try {
      const response = await api.get([this.resource, 'move'].join('/'));
      cache.remove('collection'); // Assuming cache is defined elsewhere
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

}

export default RouteService;

// Usage example:
const routeService = new RouteService();
routeService.getOne('some-id').then(data => console.log(data)).catch(error => console.error(error));