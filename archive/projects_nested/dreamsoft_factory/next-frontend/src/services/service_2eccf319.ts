import api from '@/lib/api';

class PromotionService {
  static async deleteIcon(promotionID: string): Promise<void> {
    const resource = ['promotions'];
    resource.push('uploadIcon');

    try {
      const response = await api.delete(`${resource.join('/')}/${promotionID}`);
      if (response.data.response) {
        // Assuming the 'data' object here is what you want to resolve
        return; // If no specific action needed on success, just return.
      } else {
        throw new Error('Response did not contain expected data structure.');
      }
    } catch (error: any) {
      throw error;
    }
  }
}

export default PromotionService;