import api from '@/lib/api';
import { CacheService } from '@/services/cache'; // Assume this is your cache service

class VolumeService {
  private resource: string;
  private url: string;
  private cache: CacheService;

  constructor(resource: string, url: string) {
    this.resource = resource;
    this.url = url;
    this.cache = new CacheService();
  }

  async patchVolume(volume: any): Promise<any> {
    try {
      const response = await api.patch(`${this.url}/${volume.ID}`, {
        action: 'setInvisibleVolume',
        invisible: !volume.invisible
      });

      if (response.data.response) {
        this.cache.remove(this.resource); // Remove cache for the resource
        return response.data;
      } else {
        throw new Error('Failed to patch volume');
      }
    } catch (error) {
      console.error(error);
      throw error; // Rethrow the error after logging
    }
  }

  // Other methods and properties of VolumeService...
}

export default VolumeService;