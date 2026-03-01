import api from "@/lib/api";

class ConfigService {
  private async patchResource(resource: string, form: any): Promise<any> {
    try {
      const response = await api.patch(`${process.env.API_URL}${resource}`, form);
      return response.data;
    } catch (error) {
      throw error.response?.data || new Error('An unknown error occurred');
    }
  }

  public async generateSiteMap(): Promise<void> {
    const resource = 'settings/generateSiteMap';
    try {
      const data = await api.get(`${process.env.API_URL}${resource}`);
      return data.data;
    } catch (error) {
      throw error.response?.data || new Error('An unknown error occurred');
    }
  }
}

export default ConfigService;