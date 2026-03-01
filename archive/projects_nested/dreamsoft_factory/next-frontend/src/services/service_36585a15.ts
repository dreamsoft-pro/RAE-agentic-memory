import api from '@/lib/api';

class MailTypeService {
  private static apiUrl: string;

  constructor() {
    if (!MailTypeService.apiUrl) {
      MailTypeService.apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
    }
  }

  public async get(resource: string, id: number): Promise<any> {
    try {
      const response = await api.get(`${this.apiUrl}/${resource}/${id}`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  public async variables(mailTypeID: number, data: any): Promise<any> {
    try {
      const response = await api.post(`${this.apiUrl}/${resource}/${mailTypeID}/mailVariables`, data);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  public static setApiUrl(url: string): void {
    MailTypeService.apiUrl = url;
  }
}

export default MailTypeService;