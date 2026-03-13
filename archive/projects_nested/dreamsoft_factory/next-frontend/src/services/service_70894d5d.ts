import api from '@/lib/api';
import { Cache } from '@/cache'; // Assuming cache is defined somewhere in your project

class MailTypeService {
  private resource: string = 'mailtype'; // Define resource as per requirement
  private url: string; // Initialize the URL variable

  constructor() {
    this.url = `${process.env.NEXT_PUBLIC_API_URL}/${this.resource}`;
  }

  public async update(offer: any, id?: number): Promise<any> {
    try {
      const response = await api.put(`${this.url}${id ? `/${id}` : ''}`, offer);
      if (response.data.response) {
        Cache.remove('collection');
        return response.data;
      } else {
        throw new Error(response.data.error || 'Unknown error');
      }
    } catch (error: any) {
      console.error(error);
      throw error;
    }
  }

  public async remove(id: number): Promise<any> {
    try {
      const response = await api.delete(`${this.url}/${id}`);
      if (response.data.response) {
        Cache.remove('collection');
        return response.data;
      } else {
        throw new Error(response.data.error || 'Unknown error');
      }
    } catch (error: any) {
      console.error(error);
      throw error;
    }
  }

  public static getInstance(): MailTypeService {
    if (!MailTypeService.instance) {
      MailTypeService.instance = new MailTypeService();
    }
    return MailTypeService.instance;
  }
}

const mailTypeServiceInstance = MailTypeService.getInstance();

export default mailTypeServiceInstance;