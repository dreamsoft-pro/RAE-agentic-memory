import api from '@/lib/api';

export default class RouteService {
  private resource: string;
  constructor(resource: string) {
    this.resource = resource;
  }

  public async create(data: any): Promise<any> {
    try {
      const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`, data);
      if (response.data.response) {
        // Assuming 'cache' is a global cache object and 'remove' method exists
        cache.remove('collection');
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  public async edit(elem: any): Promise<any> {
    elem.action = "edit";
    
    // Assuming 'langNames' and 'langUrls' are properties on the elem object
    elem.langNames = { ...elem.langNames };
    elem.langUrls = { ...elem.langUrls };

    console.log(elem);

    try {
      const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`, elem);
      if (response.data.response) {
        // Assuming 'cache' is a global cache object and 'remove' method exists
        cache.remove('collection');
        return response.data;
      } else {
        throw new Error(JSON.stringify(response.data));
      }
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
}