import api from '@/lib/api';

class OfferService {

  static async getFile(fileID: string, fromCompanyID?: string): Promise<string> {
    let addStr = '';
    if (fromCompanyID) {
      addStr = `?fromCompanyID=${encodeURIComponent(fromCompanyID)}`;
    }
    return `${process.env.NEXT_PUBLIC_API_URL}/offerItems/getFile/${fileID}${addStr}`;
  }

  static async removeItemFile(fileID: string): Promise<void> {
    try {
      await api.delete(`/offerItems/files/${fileID}`);
    } catch (error) {
      throw error;
    }
  }

  static async removeItem(id: string): Promise<void> {
    try {
      await api.delete(`/offerItems/${id}`);
    } catch (error) {
      throw error;
    }
  }
}