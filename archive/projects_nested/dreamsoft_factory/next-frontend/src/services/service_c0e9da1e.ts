import api from '@/lib/api';
import { rest } from 'next/rest'; // Assuming a mock import for demonstration, as there's no direct equivalent in Next.js
import type { PromiseResolver } from 'some-promise-type';

class CategoryDescriptionService {
  private apiUrl: string;

  constructor() {
    this.apiUrl = api.API_URL;
  }

  public async getAll(list: string): Promise<any> {
    const url = `${this.apiUrl}categoriesDescriptions/categoriesDescriptionsPublic?list=${encodeURIComponent(list)}`;

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Failed to fetch data:', error);
      throw error;
    }
  }
}

export default CategoryDescriptionService;