import api from '@/lib/api';

class PsPreflightFolderService {
  private resource: string;

  constructor(resource: string) {
    this.resource = resource;
  }

  public async add(item: any): Promise<any> {
    try {
      const response = await api.post(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`, item);
      
      if (response.data.response) {
        // Assuming cache is a global or instance property that needs to be removed
        this.cacheRemove(this.formatID); 
        return response.data.item;
      } else {
        throw new Error('Failed to add resource');
      }
    } catch (error: any) {
      throw error;
    }
  }

  public async edit(item: any): Promise<any> {
    try {
      const response = await api.put(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`, item);
      
      if (response.data.response) {
        this.cacheRemove(this.categoryID); 
        return response.data;
      } else {
        throw new Error('Failed to edit resource');
      }
    } catch (error: any) {
      throw error;
    }
  }

  private cacheRemove(id: string): void {
    // Implement your caching logic here, assuming it's a global or instance property
    // For example:
    // deleteCacheEntryById(id);
  }

  get formatID(): string {
    return `${this.resource}/someDynamicId`;
  }

  get categoryID(): string {
    return this.resource;
  }
}