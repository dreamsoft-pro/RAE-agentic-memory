import api from '@/lib/api';

export default class CurrencyRootService {
  private resource: string;

  constructor() {
    this.resource = 'currency'; // Example resource name, adjust as needed
  }

  public async getExchangeRates(baseCurrency: string): Promise<any> {
    const url = `/api/${this.resource}?base=${baseCurrency}`;
    try {
      const response = await api.get(url);
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch exchange rates for ${baseCurrency}:`, error);
      throw error; // Re-throw the error after logging
    }
  }

  public async setFavorite(currencyPair: string): Promise<any> {
    const url = `/api/${this.resource}/favorites?currency=${currencyPair}`;
    try {
      const response = await api.put(url); // Assuming put method is used for setting favorites, adjust as needed.
      return response.data;
    } catch (error) {
      console.error(`Failed to set ${currencyPair} as favorite:`, error);
      throw error; // Re-throw the error after logging
    }
  }

  public async getFavoritePairs(): Promise<any> {
    const url = `/api/${this.resource}/favorites`;
    try {
      const response = await api.get(url);
      return response.data;
    } catch (error) {
      console.error('Failed to fetch favorite currency pairs:', error);
      throw error; // Re-throw the error after logging
    }
  }

  public async removeFavorite(currencyPair: string): Promise<any> {
    const url = `/api/${this.resource}/favorites?currency=${currencyPair}`;
    try {
      const response = await api.delete(url); // Assuming delete method is used for removing favorites, adjust as needed.
      return response.data;
    } catch (error) {
      console.error(`Failed to remove ${currencyPair} from favorites:`, error);
      throw error; // Re-throw the error after logging
    }
  }
}