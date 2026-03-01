import api from '@/lib/api';

class OperatorService {
  private readonly apiUrl: string;

  constructor() {
    this.apiUrl = process.env.API_URL || ''; // Ensure API_URL is set or use an empty string as fallback
  }

  public async getOperator(operatorID: string, resource: string): Promise<any> {
    const url = `${this.apiUrl}/${[resource, operatorID, 'getOperator'].join('/')}`;

    try {
      const response = await api.get(url);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data || error.message);
    }
  }
}

export default OperatorService;