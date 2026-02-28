import axios from '@/lib/api';
import {Deferred} from 'ts-deferred'; // Assuming some library for deferred objects

class OfferService {
  private static async postOfferItem(item: any): Promise<any> {
    try {
      const response = await axios.post(`${process.env.API_URL}/offerItems`, item);
      if (response.data.response) {
        cache.remove('collection'); // Assuming `cache` is a global or imported object
        return response.data;
      } else {
        throw new Error('Response error');
      }
    } catch (error) {
      throw error;
    }
  }

  public static async uploadItemFile(offerItemID: string, file: File): Promise<any> {
    const formData = new FormData();
    formData.append('itemFile', file);
    
    try {
      const response = await axios.post(`${process.env.API_URL}/offerItems/files/${offerItemID}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  public static async getItemFiles(offerItemID: string): Promise<any> {
    try {
      const response = await axios.get(`${process.env.API_URL}/offerItems/files/${offerItemID}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  }
}

export default OfferService;