import api from "@/lib/api";
import { Cache } from "@/types"; // Assuming you have a Cache type defined

class ContentService {
  private resource: string;
  private routeID: string;
  private cache: Cache;

  constructor(resource: string, routeID: string, cache: Cache) {
    this.resource = resource;
    this.routeID = routeID;
    this.cache = cache;
  }

  public async getAll(force?: boolean): Promise<any> {
    if (this.cache.get('collection') && !force) {
      return this.cache.get('collection');
    } else {
      try {
        const response = await api.get(this.resource);
        this.cache.put(this.routeID, response.data);
        return response.data;
      } catch (error) {
        throw error; // Assuming you want to reject the promise with an error
      }
    }
  }

  public async move(): Promise<any> {
    try {
      const response = await api.get(this.resource);
      this.cache.remove(this.routeID);
      return response.data;
    } catch (error) {
      throw error; // Assuming you want to reject the promise with an error
    }
  }
}