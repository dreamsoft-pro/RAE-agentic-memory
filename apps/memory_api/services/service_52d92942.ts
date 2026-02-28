import api from '@/lib/api';

export default class PsPreflightFolderService {
  formatID: string;
  resource: string;
  getAllResource: string;

  constructor(formatID: string) {
    this.formatID = formatID;
    this.resource = 'ps_preflight_folder';
    this.getAllResource = `ps_preflight_folder?formatID=${this.formatID}`;
  }

  async getAll(force?: boolean): Promise<any> {
    try {
      const response = await api.get(`${process.env.NEXT_PUBLIC_API_URL}${this.getAllResource}`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : new Error('Failed to get all resources');
    }
  }

  async getAllCache(force?: boolean): Promise<any> {
    const cacheKey = this.resource;

    if (!force && process.cache[cacheKey]) {
      return process.cache[cacheKey];
    }

    try {
      const data = await this.getAll();
      process.cache[cacheKey] = data;
      return data;
    } catch (error) {
      throw error;
    }
  }
}