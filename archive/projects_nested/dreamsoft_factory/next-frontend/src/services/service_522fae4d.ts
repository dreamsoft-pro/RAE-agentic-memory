import api from '@/lib/api';

class OfferService {
  private resource: string = 'offerItems';
  private urlSegment: string = 'files';
  
  async updateFile(fileID: string, data: any): Promise<any> {
    try {
      const response = await api.put(`${process.env.NEXT_PUBLIC_API_URL}/${this.resource}/${this.urlSegment}/${fileID}`, data);
      return response.data;
    } catch (error) {
      throw error.response?.data ?? error;
    }
  }

  // You can add other methods here as needed
}

export default OfferService;

// Usage example:
// const offerService = new OfferService();
// await offerService.updateFile('123', { key: 'value' });