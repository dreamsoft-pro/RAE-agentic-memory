import api from "@/lib/api";
import { Cache } from "some-cache-library"; // Assuming cache.remove() comes from this library

class OfferService {
  private static getCacheKey(key: string): string {
    return `collection:${key}`;
  }

  public static async deleteOfferItem(id: string): Promise<void> {
    try {
      const url = `${process.env.API_URL}/offerItems/${id}`;
      await api.delete(url);
      Cache.remove(OfferService.getCacheKey("collection"));
    } catch (error) {
      throw error;
    }
  }

  public static async getCompanies(): Promise<any[]> {
    const url = `${process.env.API_URL}/offerCompanies`;
    try {
      return await api.get(url);
    } catch (error) {
      throw error;
    }
  }

  public static async create(data: any): Promise<void> {
    const url = `${process.env.API_URL}/offerItems`; // Assuming this is the URL for creating data
    try {
      await api.post(url, data);
    } catch (error) {
      throw error;
    }
  }
}

export default OfferService;