import api from '@/lib/api';

class LangService {
  constructor(private url: string) {}

  async getLanguages(): Promise<string[]> {
    if (!this.url) {
      throw new Error('URL must be defined before using this service.');
    }

    try {
      const response = await api.get(this.url);
      return response.data;
    } catch (error) {
      console.error(`Failed to fetch languages: ${error.message}`);
      throw error;
    }
  }

  // Example of another method
  async addLanguage(language: string): Promise<void> {
    if (!this.url) {
      throw new Error('URL must be defined before using this service.');
    }

    try {
      await api.post(this.url, { language });
    } catch (error) {
      console.error(`Failed to add language ${language}: ${error.message}`);
      throw error;
    }
  }
}

// Usage example
const langService = new LangService('/api/languages');
langService.getLanguages().then(languages => console.log('Available languages:', languages));