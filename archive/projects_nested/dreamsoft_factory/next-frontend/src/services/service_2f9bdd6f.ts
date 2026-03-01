import api from '@/lib/api';

class CategoryDescriptionsService {
  private resource: string;

  constructor(resource: string) {
    this.resource = resource;
  }

  public async removeDescriptionFile(fileID: string): Promise<void> {
    try {
      await api.delete(`${this.resource}/files/${fileID}`);
    } catch (error) {
      throw error.response ? error.response.data : error.message;
    }
  }
}

export default CategoryDescriptionsService;