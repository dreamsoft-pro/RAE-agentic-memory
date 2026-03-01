import api from '@/lib/api';

class VolumeService {
  private groupID: string;
  private resource: string;

  constructor(groupID: string) {
    this.groupID = groupID;
    this.resource = 'your-resource-path'; // Define the resource path here.
  }

  public async setMaxVolume(maxVolume: number): Promise<void> {
    try {
      const response = await api.post(`/api/${this.resource}/setMaxVolume`, { maxVolume });
      if (response.data.response) {
        // Assuming cacheRemove is a method you have in PsTypeService
        PsTypeService.cacheRemove(this.groupID);
      } else {
        throw new Error('Failed to set maximum volume');
      }
    } catch (error) {
      console.error(error);
      throw error;
    }
  }

  public async setStepVolume(stepVolume: number): Promise<void> {
    try {
      const response = await api.post(`/api/${this.resource}/setStepVolume`, { stepVolume });
      if (!response.data.response) {
        throw new Error('Failed to set step volume');
      }
    } catch (error) {
      console.error(error);
      throw error;
    }
  }
}

// Example usage
const service = new VolumeService('your-group-id');
service.setMaxVolume(10).catch(console.error);
service.setStepVolume(2).catch(console.error);