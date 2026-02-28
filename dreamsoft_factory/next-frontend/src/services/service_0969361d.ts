import api from '@/lib/api';

export default class SubCategoryDescriptionService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = api.API_URL; // Assuming api is an object with API_URL property
  }

  public async getAll(subcategoryURL: string): Promise<any> {
    const url = `${this.baseUrl}subcategoriesDescriptions/subcategoriesDescriptionsPublic?categoryURL=${subcategoryURL}`;
    try {
      const response = await fetch(url);
      if (!response.ok) throw new Error('Failed to fetch data');
      return await response.json();
    } catch (error) {
      throw error;
    }
  }
}