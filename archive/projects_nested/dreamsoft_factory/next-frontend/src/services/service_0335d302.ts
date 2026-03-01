import api from '@/lib/api';

class TypeDescriptionsService {
  private apiUrl: string;

  constructor(config: { API_URL: string }) {
    this.apiUrl = config.API_URL;
  }

  public async removeDescriptionFile(fileID: string): Promise<void> {
    const url = `${this.apiUrl}/${'resource'}/files/${fileID}`;
    
    try {
      await api.delete(url);
    } catch (error) {
      throw error; // or handle the error appropriately
    }
  }
}

export default TypeDescriptionsService;