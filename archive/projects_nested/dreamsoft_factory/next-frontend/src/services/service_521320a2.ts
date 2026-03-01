import axios from '@/lib/api';

class PrintTypeService {
  private resource: string;

  constructor(resource: string) {
    this.resource = resource;
  }

  async updatePrintTypeDevices(printtypeId: number, devices: any): Promise<any> {
    const url = `${process.env.API_URL}/${this.getResource()}/${printtypeId}/ps_printtypeDevices`;
    
    try {
      const response = await axios.patch(url, devices);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }

  private getResource(): string {
    // Implementation of this method is needed. For demonstration purposes, let's assume it returns 'printtype'.
    return 'printtype';
  }
}

export default PrintTypeService;