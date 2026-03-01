import api from '@/lib/api';

class PsTypeDescriptionService {
  private apiUrl: string;

  constructor() {
    this.apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
  }

  public async getAll(groupID: number, typeID: number): Promise<any> {
    try {
      const response = await api.get(`${this.apiUrl}ps_typeDescriptions/typeDescriptionsPublic?groupID=${groupID}&typeID=${typeID}`);
      return response.data;
    } catch (error) {
      throw error.response ? error.response : error;
    }
  }
}

export default PsTypeDescriptionService;

// Usage Example:
// const service = new PsTypeDescriptionService();
// service.getAll(1, 2).then(data => console.log(data)).catch(error => console.error('Error:', error));