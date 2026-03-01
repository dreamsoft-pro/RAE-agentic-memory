import api from "@/lib/api";
import { Cache } from "memory-cache";

export default class PsConfigIncreaseTypeService {
  private cache: Cache;

  constructor() {
    this.cache = new Cache();
  }

  public async getAll(force?: boolean): Promise<any[]> {
    let collectionKey = 'ps_config_increaseTypes';
    
    if (!force && this.cache.get(collectionKey)) {
      return this.cache.get(collectionKey);
    }
    
    try {
      const response = await api.get('ps_config_increase_types');
      const collection = response.data;
      
      this.cache.put(collectionKey, collection, null); // Cache indefinitely
      
      if (force) {
        window.dispatchEvent(new Event('ps_config_increaseTypes')); // Simulating $rootScope.$emit
      }
      
      return collection;
    } catch (error) {
      throw error; // Rejecting with the original error
    }
  }
}